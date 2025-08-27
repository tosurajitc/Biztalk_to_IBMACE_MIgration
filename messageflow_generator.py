"""
Program 2: 
clean_ace_generator.py - MessageFlow Generator with BizTalk .btm Processing
100% LLM-based with actual BizTalk transformation logic integration
"""
import os
import json
import pandas as pd
import xml.etree.ElementTree as ET
from typing import Dict, List
from datetime import datetime
from groq import Groq
from pathlib import Path


class MessageFlowGenerationError(Exception):
    """Exception for MessageFlow generation failures"""
    pass


class StreamlinedACEGenerator:
    """100% LLM MessageFlow Generator with BizTalk .btm file processing"""
    
    def __init__(self, app_name: str, flow_name: str, groq_api_key: str, groq_model: str):
        self.app_name = app_name
        self.flow_name = flow_name
        self.client = Groq(api_key=groq_api_key)
        self.groq_model = groq_model
        print(f"🎯 MessageFlow Generator Ready: {flow_name} | Model: {groq_model}")
    
    def generate_messageflow(self, component_mapping: pd.DataFrame, msgflow_template: str, 
                           confluence_spec: str, biztalk_maps_path: str, output_dir: str) -> Dict:
        """Generate MessageFlow with BizTalk .btm file processing"""
        print("🚀 Starting MessageFlow Generation with BizTalk Maps Processing")
        
        try:
            # Validate inputs
            self._validate_inputs(component_mapping, msgflow_template, confluence_spec, biztalk_maps_path)
            
            # Process BizTalk Maps (.btm files)
            print(f"📁 Processing BizTalk Maps from: {biztalk_maps_path}")
            biztalk_maps = self._process_biztalk_maps(biztalk_maps_path)
            print(f"   📊 Found {len(biztalk_maps)} BizTalk map files")
            
            # Process business requirements
            business_context = self._process_business_requirements(confluence_spec)
            
            # Process component mappings
            component_context = self._process_components(component_mapping)
            
            # Generate MessageFlow XML with BizTalk context
            msgflow_file = self._generate_xml_with_biztalk(
                msgflow_template, business_context, component_context, biztalk_maps, output_dir
            )
            
            # Validate output
            validation = self._validate_xml(msgflow_file)
            if not validation['valid']:
                raise MessageFlowGenerationError(f"Generated XML validation failed: {validation['errors']}")
            
            print("✅ MessageFlow generation completed successfully")
            return {
                'success': True,
                'messageflow_file': msgflow_file,
                'biztalk_maps_processed': len(biztalk_maps),
                'validation': validation,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"MessageFlow generation failed: {str(e)}"
            print(f"❌ {error_msg}")
            raise MessageFlowGenerationError(error_msg)
    
    def _validate_inputs(self, component_mapping: pd.DataFrame, msgflow_template: str, 
                        confluence_spec: str, biztalk_maps_path: str):
        """Validate all inputs including BizTalk maps path"""
        errors = []
        
        if component_mapping.empty:
            errors.append("Component mapping is empty")
        if not msgflow_template or not msgflow_template.strip():
            errors.append("MessageFlow template is missing")
        if not confluence_spec or not confluence_spec.strip():
            errors.append("Confluence specification is missing")
        if not biztalk_maps_path or not os.path.exists(biztalk_maps_path):
            errors.append(f"BizTalk maps path does not exist: {biztalk_maps_path}")
        
        required_cols = ['biztalk_component', 'required_ace_library', 'component_type']
        missing_cols = [col for col in required_cols if col not in component_mapping.columns]
        if missing_cols:
            errors.append(f"Missing columns: {missing_cols}")
        
        if errors:
            raise MessageFlowGenerationError("Input validation failed: " + "; ".join(errors))
    
    def _process_biztalk_maps(self, biztalk_maps_path: str) -> List[Dict]:
        """Process all .btm files in the specified path"""
        try:
            maps_data = []
            btm_files = list(Path(biztalk_maps_path).glob("*.btm"))
            
            if not btm_files:
                print(f"⚠️ No .btm files found in {biztalk_maps_path}")
                return []
            
            for btm_file in btm_files:
                try:
                    print(f"   🔍 Processing: {btm_file.name}")
                    map_content = self._extract_btm_content(btm_file)
                    if map_content:
                        maps_data.append(map_content)
                except Exception as e:
                    print(f"   ⚠️ Error processing {btm_file.name}: {str(e)}")
                    continue
            
            return maps_data
            
        except Exception as e:
            raise MessageFlowGenerationError(f"BizTalk maps processing failed: {str(e)}")
    
    def _extract_btm_content(self, btm_file: Path) -> Dict:
        """Extract transformation logic from a single .btm file"""
        try:
            with open(btm_file, 'r', encoding='utf-8') as f:
                btm_content = f.read()
            
            # Use LLM to extract transformation logic from .btm XML
            prompt = f"""Analyze this BizTalk Map (.btm) file and extract transformation logic:

File: {btm_file.name}
Content: {btm_content[:3000]}...

Extract and return JSON with:
{{
    "map_name": "map name",
    "source_schema": "source schema name", 
    "target_schema": "target schema name",
    "transformations": [
        {{"source_field": "field1", "target_field": "field2", "operation": "copy/transform/concat"}},
        {{"operation": "custom", "logic": "transformation logic description"}}
    ],
    "business_rules": ["rule1", "rule2"],
    "error_handling": ["error pattern1", "error pattern2"]
}}

Return only JSON:"""
            
            response = self.client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {"role": "system", "content": "You are a BizTalk expert. Extract transformation logic from .btm files as structured JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1500
            )
            
            result = response.choices[0].message.content.strip()
            try:
                parsed_result = json.loads(result)
                parsed_result["file_name"] = btm_file.name
                return parsed_result
            except json.JSONDecodeError:
                return {
                    "file_name": btm_file.name,
                    "map_name": btm_file.stem,
                    "raw_analysis": result[:500],
                    "transformations": [],
                    "business_rules": []
                }
                
        except Exception as e:
            print(f"   ❌ Failed to extract from {btm_file.name}: {str(e)}")
            return None
    
    def _process_business_requirements(self, confluence_spec: str) -> Dict:
        """Extract business requirements using LLM"""
        try:
            prompt = f"""Extract key MessageFlow requirements from this specification:

{confluence_spec[:2000]}

Return JSON with:
- business_purpose
- integration_requirements  
- error_handling_needs
- performance_requirements

JSON only:"""
            
            response = self.client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {"role": "system", "content": "Extract MessageFlow requirements as JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=800
            )
            
            result = response.choices[0].message.content.strip()
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"business_purpose": "MessageFlow based on provided spec", "raw_content": result[:300]}
                
        except Exception as e:
            raise MessageFlowGenerationError(f"Business requirements processing failed: {str(e)}")
    
    def _process_components(self, component_mapping: pd.DataFrame) -> List[Dict]:
        """Process component mappings for context"""
        components = []
        for _, row in component_mapping.iterrows():
            components.append({
                "biztalk_component": str(row.get('biztalk_component', '')),
                "component_type": str(row.get('component_type', '')),
                "ace_library": str(row.get('required_ace_library', '')),
                "notes": str(row.get('migration_notes', ''))
            })
        return components
    
    def _generate_xml_with_biztalk(self, msgflow_template: str, business_context: Dict, 
                                  component_context: List[Dict], biztalk_maps: List[Dict], 
                                  output_dir: str) -> str:
        """Generate MessageFlow XML with BizTalk transformation context"""
        try:
            # Import prompt functions
            from prompt_module import get_msgflow_generation_prompt, PromptModule
            
            # Prepare ESQL modules from components and BizTalk maps
            esql_modules = []
            
            # Add modules from component mapping
            for comp in component_context:
                if comp['ace_library']:
                    esql_modules.append({
                        "name": comp['ace_library'],
                        "purpose": f"Process {comp['biztalk_component']}"
                    })
            
            # Add modules from BizTalk maps
            for btm_map in biztalk_maps:
                esql_modules.append({
                    "name": f"ESQL_{btm_map.get('map_name', 'Transform')}",
                    "purpose": f"Transform using {btm_map.get('file_name', 'BizTalk map')}",
                    "transformations": btm_map.get('transformations', []),
                    "business_rules": btm_map.get('business_rules', [])
                })
            
            # Generate enhanced prompt with BizTalk context
            confluence_text = business_context.get('raw_content', '') or json.dumps(business_context)
            
            # Create comprehensive prompt with BizTalk map details
            enhanced_prompt = self._create_enhanced_prompt_with_biztalk(
                msgflow_template, confluence_text, component_context, biztalk_maps, esql_modules
            )
            
            # Call LLM with expert system context
            prompt_module = PromptModule()
            response = self.client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {"role": "system", "content": prompt_module.get_system_context()},
                    {"role": "user", "content": enhanced_prompt}
                ],
                temperature=0.1,
                max_tokens=6000
            )
            
            # Process response
            xml_content = response.choices[0].message.content.strip()
            if xml_content.startswith("```xml"):
                xml_content = xml_content.replace("```xml", "").replace("```", "").strip()
            if not xml_content.startswith("<?xml"):
                xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_content
            
            # Save file
            os.makedirs(output_dir, exist_ok=True)
            msgflow_file = os.path.join(output_dir, f"{self.flow_name}.msgflow")
            with open(msgflow_file, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            
            print(f"📄 Generated: {os.path.basename(msgflow_file)}")
            return msgflow_file
            
        except Exception as e:
            raise MessageFlowGenerationError(f"XML generation failed: {str(e)}")
    
    def _create_enhanced_prompt_with_biztalk(self, msgflow_template: str, confluence_spec: str,
                                           component_context: List[Dict], biztalk_maps: List[Dict],
                                           esql_modules: List[Dict]) -> str:
        """Create comprehensive prompt including BizTalk transformation logic"""
        
        prompt = f"""# IBM ACE MessageFlow Generation with BizTalk Integration

Generate a production-ready MessageFlow XML for: {self.flow_name}

## 🎯 MESSAGEFLOW TEMPLATE:
```xml
{msgflow_template[:1500]}
```

## 📋 BUSINESS REQUIREMENTS:
{confluence_spec[:1000]}

## 🔄 BIZTALK TRANSFORMATION MAPS:
"""
        
        # Add BizTalk map details
        for i, btm_map in enumerate(biztalk_maps[:5]):  # Limit to 5 maps for token efficiency
            prompt += f"""
### Map {i+1}: {btm_map.get('file_name', 'Unknown')}
- **Source Schema**: {btm_map.get('source_schema', 'N/A')}
- **Target Schema**: {btm_map.get('target_schema', 'N/A')}
- **Transformations**: {json.dumps(btm_map.get('transformations', [])[:3])}  # Top 3 transformations
- **Business Rules**: {btm_map.get('business_rules', [])}
"""
        
        prompt += f"""

## 🛠️ COMPONENT MAPPINGS:
{json.dumps(component_context[:8], indent=2)}

## 🎯 CRITICAL GENERATION REQUIREMENTS:

### 1. XML Structure (MANDATORY):
- Use template as EXACT foundation
- Preserve ALL xmlns namespace declarations  
- Maintain node ID patterns (FCMComposite_1_1, etc.)
- Keep connection terminal naming exactly as template

### 2. BizTalk Integration Rules:
- Convert BizTalk Map transformations to ESQL Compute nodes
- Implement transformation logic from .btm files in ESQL format
- Preserve business rules from BizTalk maps
- Map source/target schemas to ACE message models

### 3. Required Elements:
- Add <propertyOrganizer/> AFTER </composition>
- Add <stickyBoard/> AFTER </composition>
- Include graphic resources BEFORE <composition>:
```xml
<colorGraphic16 xmi:type="utility:GIFFileGraphic" resourceName="platform:/plugin/{self.app_name}/icons/full/obj16/{self.flow_name}.gif"/>
<colorGraphic32 xmi:type="utility:GIFFileGraphic" resourceName="platform:/plugin/{self.app_name}/icons/full/obj30/{self.flow_name}.gif"/>
```

### 4. Transformation Implementation:
- Create Compute nodes for each BizTalk map transformation
- Implement field mappings using ESQL syntax
- Include business rule logic in ESQL
- Add proper error handling for transformations

### 5. Validation Requirements:
- ALL nodes must have valid connections
- ALL xmi:id values must be unique
- ALL terminal references must exist
- XML must be well-formed and parseable

## OUTPUT:
Generate ONLY the complete MessageFlow XML. No explanations.

```xml"""
        
        return prompt
    
    def _validate_xml(self, msgflow_file: str) -> Dict:
        """Validate generated XML"""
        try:
            with open(msgflow_file, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            
            # Test XML parsing
            try:
                ET.fromstring(xml_content)
                xml_valid = True
                errors = []
            except ET.ParseError as e:
                xml_valid = False
                errors = [f"XML Parse Error: {str(e)}"]
            
            # Check required elements
            required = ['<propertyOrganizer/>', '<stickyBoard/>']
            for element in required:
                if element not in xml_content:
                    errors.append(f"Missing: {element}")
            
            valid = xml_valid and len(errors) == 0
            return {'valid': valid, 'errors': errors}
            
        except Exception as e:
            return {'valid': False, 'errors': [f"Validation failed: {str(e)}"]}


def run_messageflow_generator(mapping_file: str, msgflow_template_content: str, confluence_content: str,
                            biztalk_maps_path: str, app_name: str, flow_name: str, 
                            groq_api_key: str, groq_model: str) -> Dict:
    """Main execution function with BizTalk maps processing"""
    try:
        print("📊 Loading component mapping...")
        component_mapping_df = pd.read_excel(mapping_file, sheet_name='Component Mapping')
        
        generator = StreamlinedACEGenerator(app_name, flow_name, groq_api_key, groq_model)
        output_dir = os.path.join(os.path.dirname(mapping_file), f"MessageFlow_{app_name}")
        
        return generator.generate_messageflow(
            component_mapping=component_mapping_df,
            msgflow_template=msgflow_template_content,
            confluence_spec=confluence_content,
            biztalk_maps_path=biztalk_maps_path,
            output_dir=output_dir
        )
        
    except MessageFlowGenerationError:
        raise
    except Exception as e:
        raise MessageFlowGenerationError(f"Execution failed: {str(e)}")


def create_messageflow_generator(app_name: str, flow_name: str, groq_api_key: str, groq_model: str):
    """Factory function"""
    return StreamlinedACEGenerator(app_name, flow_name, groq_api_key, groq_model)