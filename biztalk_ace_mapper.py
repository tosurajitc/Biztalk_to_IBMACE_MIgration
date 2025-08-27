#!/usr/bin/env python3
"""
Program 1:
Smart Hybrid BizTalk to ACE Mapper
LLM for .project files + Rule-based for .esql files
Fast, reliable, and intelligent
"""

import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import re
import time

try:
    from groq import Groq
    from prompt_module import PromptModule
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Install with: pip install groq")
    exit(1)


class SmartBizTalkMapper:
    """Hybrid Smart BizTalk to ACE mapper with LLM + Rule-based intelligence"""
    
    def __init__(self):
        # FIRST: Initialize all required attributes BEFORE calling any methods
        self.progress_callback = None  # MUST BE FIRST - before any _log calls
        self.biztalk_components = []
        self.ace_components = []
        self.intelligent_mappings = []
        
        # Config
        self.model = "llama3-70b-8192"
        self.temperature = 0.1
        
        # LLM setup - initialized as None first
        self.llm = None
        self.prompt_module = None
        self.llm_enabled = False
        
        # Performance settings
        self.max_files_per_type = 50  # Reasonable limit per file type
        self.llm_timeout = 30  # 30 seconds timeout per LLM call
        self.max_content_size = 1000  # Reduced content size
        
        # Rule-based patterns for ESQL analysis
        self.esql_patterns = {
            'database': re.compile(r'(DATABASE|PASSTHRU|SELECT|INSERT|UPDATE|DELETE)', re.IGNORECASE),
            'http': re.compile(r'(HTTPRequest|HTTPReply|REST|SOAP|WebService)', re.IGNORECASE),
            'transformation': re.compile(r'(TRANSFORM|MAP|CONVERT|FORMAT)', re.IGNORECASE),
            'validation': re.compile(r'(VALIDATE|CHECK|VERIFY|ASSERT)', re.IGNORECASE),
            'routing': re.compile(r'(ROUTE|SWITCH|CASE|WHEN)', re.IGNORECASE),
            'logging': re.compile(r'(LOG|TRACE|DEBUG|AUDIT)', re.IGNORECASE),
            'error': re.compile(r'(ERROR|EXCEPTION|TRY|CATCH|THROW)', re.IGNORECASE),
            'message': re.compile(r'(MESSAGE|PAYLOAD|HEADER|PROPERTY)', re.IGNORECASE)
        }
        
        # LAST: Initialize LLM after all attributes are set
        self._initialize_llm()

    def _initialize_llm(self):
        """Initialize LLM with error handling - SAFE VERSION"""
        api_key = os.getenv('GROQ_API_KEY')
        if api_key:
            try:
                self.llm = Groq(api_key=api_key)
                self.prompt_module = PromptModule()
                self.llm_enabled = True
                self._log("🧠 Hybrid analysis enabled (LLM + Rules)")
            except Exception as e:
                self.llm_enabled = False
                self._log(f"⚠️ LLM initialization failed: {e}")
        else:
            self.llm_enabled = False
            self._log("❌ GROQ_API_KEY not found - using rule-based only")

    def set_progress_callback(self, callback):
        """Set progress callback for UI - MAIN.PY COMPATIBILITY"""
        self.progress_callback = callback
        
    def _log(self, message: str):
        """Simple logging with timestamp - MAIN.PY COMPATIBILITY"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        
        # Call progress callback if set (for main.py UI)
        if self.progress_callback:
            self.progress_callback(message)
            
        # Also print to console
        print(log_message)



    def scan_biztalk(self, path: str, file_extensions: List[str] = None):
        """Scan and analyze BizTalk components with file-level granularity - ENHANCED"""
        self._log("🔍 Analyzing BizTalk components...")
        
        # Use provided extensions or prioritized defaults
        if file_extensions:
            extensions = set(ext.lower() for ext in file_extensions)
        else:
            # Prioritize important files
            extensions = {'.odx', '.btm', '.xsd', '.btp', '.btproj', '.sln', '.cs', '.config', '.xml', '.xsl'}
        
        # Smart file discovery
        biztalk_files = self._discover_files_smart(path, extensions)
        self._log(f"📂 Found {len(biztalk_files)} BizTalk files to analyze")
        
        self.biztalk_components = []
        processed_count = 0
        
        for file_path in biztalk_files:
            try:
                # File-specific analysis based on extension
                ext = file_path.suffix.lower()
                
                # Basic file information
                analysis = {
                    'name': file_path.stem,
                    'file_name': file_path.name,
                    'full_path': str(file_path),
                    'relative_path': str(file_path.relative_to(Path(path))),
                    'file_extension': ext,
                    'size_bytes': file_path.stat().st_size,
                    'last_modified': file_path.stat().st_mtime,
                    'analysis_method': 'file_specific'
                }
                
                # File-type-specific details
                if ext == '.odx':
                    analysis.update({
                        'type': 'BizTalk Orchestration',
                        'ace_equivalent': 'Message Flow (.msgflow)',
                        'ace_mapping_target': f"{file_path.stem}.msgflow",
                        'complexity': 'HIGH',
                        'migration_priority': 1,
                        'critical_for_migration': True
                    })
                elif ext == '.btm':
                    analysis.update({
                        'type': 'BizTalk Map',
                        'ace_equivalent': 'Mapping Node + Message Map (.map)',
                        'ace_mapping_target': f"{file_path.stem}.map",
                        'complexity': 'MEDIUM',
                        'migration_priority': 2,
                        'critical_for_migration': True
                    })
                elif ext == '.xsd':
                    analysis.update({
                        'type': 'XML Schema',
                        'ace_equivalent': 'Message Model (.xsd/.mxsd)',
                        'ace_mapping_target': f"{file_path.stem}.xsd",
                        'complexity': 'LOW',
                        'migration_priority': 2,
                        'critical_for_migration': True
                    })
                elif ext == '.btp':
                    analysis.update({
                        'type': 'BizTalk Pipeline',
                        'ace_equivalent': 'Message Flow with Pipeline Stages',
                        'ace_mapping_target': f"{file_path.stem}_Pipeline.msgflow",
                        'complexity': 'MEDIUM',
                        'migration_priority': 3,
                        'critical_for_migration': True
                    })
                elif ext == '.btproj':
                    analysis.update({
                        'type': 'BizTalk Project',
                        'ace_equivalent': 'ACE Application (.appproject)',
                        'ace_mapping_target': f"{file_path.stem}.appproject",
                        'complexity': 'LOW',
                        'migration_priority': 1,
                        'critical_for_migration': True
                    })
                elif ext == '.sln':
                    analysis.update({
                        'type': 'Solution File',
                        'ace_equivalent': 'IBM Integration Toolkit Workspace',
                        'ace_mapping_target': f"{file_path.stem}.workspace",
                        'complexity': 'LOW',
                        'migration_priority': 1,
                        'critical_for_migration': True
                    })
                elif ext == '.cs':
                    analysis.update({
                        'type': 'C# Source Code',
                        'ace_equivalent': 'Java Classes (.java) or ESQL (.esql)',
                        'ace_mapping_target': f"{file_path.stem}.java",
                        'complexity': 'HIGH',
                        'migration_priority': 4,
                        'critical_for_migration': False
                    })
                elif ext == '.config':
                    analysis.update({
                        'type': 'Configuration File',
                        'ace_equivalent': 'Configurable Services (.properties)',
                        'ace_mapping_target': f"{file_path.stem}.properties",
                        'complexity': 'LOW',
                        'migration_priority': 5,
                        'critical_for_migration': False
                    })
                elif ext == '.xsl' or ext == '.xslt':
                    analysis.update({
                        'type': 'XSLT Transform',
                        'ace_equivalent': 'XSLTransform Node or ESQL Transform',
                        'ace_mapping_target': f"{file_path.stem}.esql",
                        'complexity': 'MEDIUM',
                        'migration_priority': 3,
                        'critical_for_migration': True
                    })
                elif ext == '.xml':
                    analysis.update({
                        'type': 'XML Configuration/Data',
                        'ace_equivalent': 'Configuration or Test Data',
                        'ace_mapping_target': f"{file_path.stem}_config.xml",
                        'complexity': 'LOW',
                        'migration_priority': 5,
                        'critical_for_migration': False
                    })
                else:
                    analysis.update({
                        'type': 'Other File',
                        'ace_equivalent': 'Manual Review Required',
                        'ace_mapping_target': f"{file_path.name}",
                        'complexity': 'UNKNOWN',
                        'migration_priority': 6,
                        'critical_for_migration': False
                    })
                
                # Add common migration fields
                analysis.update({
                    'migration_notes': f"File-level mapping: {analysis['type']} → {analysis['ace_equivalent']}",
                    'requires_manual_review': analysis['complexity'] == 'HIGH',
                    'estimated_effort_hours': {
                        'LOW': 1, 'MEDIUM': 4, 'HIGH': 8, 'UNKNOWN': 2
                    }.get(analysis['complexity'], 2)
                })
                
                self.biztalk_components.append(analysis)
                processed_count += 1
                
                # Progress update every 10 files
                if processed_count % 10 == 0:
                    self._log(f"📊 Processed {processed_count}/{len(biztalk_files)} BizTalk files")
                    
            except Exception as e:
                self._log(f"⚠️ Skipping {file_path.name}: {e}")
                continue
        
        # Summary by component type
        component_summary = {}
        for component in self.biztalk_components:
            comp_type = component.get('type', 'Unknown')
            component_summary[comp_type] = component_summary.get(comp_type, 0) + 1
        
        self._log(f"✅ Analyzed {len(self.biztalk_components)} BizTalk components:")
        for comp_type, count in component_summary.items():
            self._log(f"   • {comp_type}: {count} files")
        
        # Log critical files found
        critical_files = [c for c in self.biztalk_components if c.get('critical_for_migration', False)]
        self._log(f"🎯 Found {len(critical_files)} critical files for migration")

    def scan_ace_libraries(self, path: str):
        """Hybrid analysis: LLM for .project files, Rules for .esql files"""
        self._log("🔍 Starting hybrid ACE library analysis...")
        
        ace_root = Path(path)
        if not ace_root.exists():
            self._log(f"❌ ACE path not found: {path}")
            return
        
        self.ace_components = []
        
        # Step 1: Find all library projects
        project_files = list(ace_root.rglob('*.project'))
        self._log(f"📋 Found {len(project_files)} library projects")
        
        # Step 2: Analyze each library using hybrid approach
        for project_file in project_files:
            try:
                library_analysis = self._analyze_library_hybrid(project_file)
                if library_analysis:
                    self.ace_components.append(library_analysis)
                    self._log(f"✅ Analyzed library: {library_analysis.get('name', 'Unknown')}")
            except Exception as e:
                self._log(f"⚠️ Failed to analyze {project_file.name}: {e}")
                continue
        
        self._log(f"🎯 Completed hybrid analysis: {len(self.ace_components)} libraries")

    def _discover_files_smart(self, path: str, extensions: set) -> List[Path]:
        """Smart file discovery with limits and prioritization"""
        path_obj = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        
        # Discover all matching files
        all_files = []
        for file_path in path_obj.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in extensions:
                all_files.append(file_path)
        
        # Group by extension for smart limiting
        files_by_type = {}
        for file_path in all_files:
            ext = file_path.suffix.lower()
            if ext not in files_by_type:
                files_by_type[ext] = []
            files_by_type[ext].append(file_path)
        
        # Apply limits and prioritization
        selected_files = []
        priority_order = ['.odx', '.btm', '.xsd', '.btp', '.btproj', '.cs', '.config']
        
        for ext in priority_order:
            if ext in files_by_type:
                # Limit files per type to prevent overload
                limited_files = files_by_type[ext][:self.max_files_per_type]
                selected_files.extend(limited_files)
                
                if len(files_by_type[ext]) > self.max_files_per_type:
                    self._log(f"📝 Limited {ext} files to {self.max_files_per_type} (found {len(files_by_type[ext])})")
        
        return selected_files

    def _analyze_library_hybrid(self, project_file: Path) -> Optional[Dict]:
        """Hybrid library analysis: LLM for .project + Rules for .esql"""
        library_dir = project_file.parent
        library_name = library_dir.name
        
        # Step 1: LLM Analysis of .project file
        project_analysis = self._analyze_project_with_llm(project_file)
        if not project_analysis:
            self._log(f"⚠️ Failed LLM analysis for {library_name}")
            project_analysis = {'name': library_name, 'purpose': 'Unknown', 'capabilities': []}
        
        # Step 2: Rule-based analysis of .esql files
        esql_analysis = self._analyze_esql_files_with_rules(library_dir)
        
        # Step 3: Combine analyses
        combined_analysis = {
            'name': library_name,
            'path': str(library_dir),
            'type': 'ACE Library',
            'business_purpose': project_analysis.get('purpose', 'Unknown'),
            'business_capabilities': project_analysis.get('capabilities', []),
            'technical_patterns': esql_analysis.get('patterns', []),
            'esql_modules': esql_analysis.get('modules', []),
            'complexity': esql_analysis.get('complexity', 'MEDIUM'),
            'reusability': project_analysis.get('reusability', 'MEDIUM'),
            'analysis_method': 'hybrid',
            'project_analysis': project_analysis,
            'esql_analysis': esql_analysis
        }
        
        return combined_analysis

    def _analyze_project_with_llm(self, project_file: Path) -> Optional[Dict]:
        """LLM analysis of .project file for business understanding"""
        if not self.llm_enabled:
            return None
        
        try:
            # Read project file content
            content = project_file.read_text(encoding='utf-8', errors='ignore')
            
            # Create focused prompt for project analysis
            prompt = f"""Analyze this ACE library project file for business understanding:

Project: {project_file.name}
Content: {content[:self.max_content_size]}

Extract business information and return JSON:
{{
    "name": "library name",
    "purpose": "business purpose and domain",
    "capabilities": ["business", "capabilities", "provided"],
    "reusability": "HIGH/MEDIUM/LOW",
    "domain": "business domain (finance, logistics, etc.)"
}}

Focus on business purpose, not technical implementation."""
            
            # LLM call with timeout protection
            start_time = time.time()
            response = self.llm.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a business analyst extracting business purpose from ACE library projects."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=500  # Reduced for faster processing
            )
            
            elapsed_time = time.time() - start_time
            if elapsed_time > self.llm_timeout:
                self._log(f"⏰ LLM timeout for {project_file.name}")
                return None
            
            return self._parse_json_response(response.choices[0].message.content)
            
        except Exception as e:
            self._log(f"⚠️ LLM project analysis failed for {project_file.name}: {e}")
            return None

    def _analyze_esql_files_with_rules(self, library_dir: Path) -> Dict:
        """Rule-based analysis of .esql files for technical patterns"""
        esql_files = list(library_dir.rglob('*.esql'))
        
        if not esql_files:
            return {'patterns': [], 'modules': [], 'complexity': 'LOW'}
        
        detected_patterns = set()
        modules = []
        total_lines = 0
        
        for esql_file in esql_files[:20]:  # Limit to prevent overload
            try:
                content = esql_file.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                total_lines += len(lines)
                
                # Pattern detection using regex
                file_patterns = []
                for pattern_name, pattern_regex in self.esql_patterns.items():
                    if pattern_regex.search(content):
                        detected_patterns.add(pattern_name)
                        file_patterns.append(pattern_name)
                
                # Extract module information
                module_info = {
                    'name': esql_file.stem,
                    'file': esql_file.name,
                    'patterns': file_patterns,
                    'lines': len(lines)
                }
                modules.append(module_info)
                
            except Exception as e:
                self._log(f"⚠️ Failed to analyze {esql_file.name}: {e}")
                continue
        
        # Determine complexity based on patterns and size
        complexity = 'LOW'
        if len(detected_patterns) > 4 or total_lines > 2000:
            complexity = 'HIGH'
        elif len(detected_patterns) > 2 or total_lines > 500:
            complexity = 'MEDIUM'
        
        return {
            'patterns': list(detected_patterns),
            'modules': modules,
            'complexity': complexity,
            'total_esql_files': len(esql_files),
            'total_lines': total_lines
        }

    def _analyze_with_llm_safe(self, file_path: Path, component_type: str) -> Optional[Dict]:
        """Safe LLM analysis with timeout and error handling"""
        if not self.llm_enabled:
            return self._analyze_with_basic_rules(file_path, component_type)
        
        try:
            # Quick content read with size limit
            content = ""
            if file_path.suffix.lower() in ['.cs', '.xml', '.xsd', '.config']:
                content = file_path.read_text(encoding='utf-8', errors='ignore')[:self.max_content_size]
            
            # Simple, fast prompt
            prompt = f"""Quick analysis of {component_type} component:

File: {file_path.name} ({file_path.suffix})
Content: {content[:300] if content else "Binary file"}

Return JSON:
{{
    "name": "{file_path.stem}",
    "type": "component type",
    "purpose": "brief purpose",
    "complexity": "LOW/MEDIUM/HIGH"
}}"""
            
            # Fast LLM call
            start_time = time.time()
            response = self.llm.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"Quick {component_type} component analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,  # More deterministic
                max_tokens=300    # Faster response
            )
            
            elapsed_time = time.time() - start_time
            if elapsed_time > 10:  # Quick timeout
                self._log(f"⏰ Quick timeout for {file_path.name}")
                return self._analyze_with_basic_rules(file_path, component_type)
            
            result = self._parse_json_response(response.choices[0].message.content)
            if result:
                result['path'] = str(file_path)
                result['size'] = file_path.stat().st_size
                result['analysis_method'] = 'llm'
                return result
            
        except Exception as e:
            self._log(f"⚠️ LLM analysis failed for {file_path.name}, using rules: {e}")
        
        # Fallback to basic rule-based analysis
        return self._analyze_with_basic_rules(file_path, component_type)

    def _analyze_with_basic_rules(self, file_path: Path, component_type: str) -> Dict:
        """Basic rule-based analysis as fallback"""
        ext = file_path.suffix.lower()
        
        # Basic type mapping
        type_mapping = {
            '.odx': 'Orchestration',
            '.btm': 'Map', 
            '.xsd': 'Schema',
            '.btp': 'Pipeline',
            '.btproj': 'Project',
            '.cs': 'C# Code',
            '.config': 'Configuration',
            '.msgflow': 'Message Flow',
            '.esql': 'ESQL Module',
            '.subflow': 'Subflow',
            '.java': 'Java Compute'
        }
        
        return {
            'name': file_path.stem,
            'type': type_mapping.get(ext, 'Unknown'),
            'purpose': f'Basic {type_mapping.get(ext, "component")} analysis',
            'complexity': 'MEDIUM',
            'path': str(file_path),
            'size': file_path.stat().st_size,
            'analysis_method': 'rules'
        }

    def _parse_json_response(self, response_text: str) -> Optional[Dict]:
        """Parse JSON from LLM response with error handling"""
        try:
            # Extract JSON from response
            if '```json' in response_text:
                start = response_text.find('```json') + 7
                end = response_text.find('```', start)
                json_text = response_text[start:end].strip()
            elif '{' in response_text and '}' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_text = response_text[start:end]
            else:
                return None
            
            return json.loads(json_text)
            
        except json.JSONDecodeError:
            return None
        except Exception:
            return None

    def create_mappings(self):
        """Create intelligent mappings using hybrid approach"""
        self._log("🧠 Creating intelligent mappings...")
        
        if not self.biztalk_components or not self.ace_components:
            self._log("❌ No components to map")
            return
        
        self.intelligent_mappings = []
        
        for biz_component in self.biztalk_components:
            try:
                mapping = self._create_smart_mapping_fast(biz_component)
                if mapping:
                    self.intelligent_mappings.append(mapping)
            except Exception as e:
                self._log(f"⚠️ Mapping failed for {biz_component.get('name', 'Unknown')}: {e}")
                continue
        
        self._log(f"✅ Created {len(self.intelligent_mappings)} intelligent mappings")

    def _create_smart_mapping_fast(self, biztalk_component: Dict) -> Optional[Dict]:
        """Fast mapping creation with simplified logic"""
        
        # Quick rule-based pre-filtering
        best_matches = self._find_matches_by_rules(biztalk_component)
        
        if self.llm_enabled and len(best_matches) > 1:
            # Use LLM only for complex decisions
            return self._refine_mapping_with_llm(biztalk_component, best_matches)
        else:
            # Use rule-based mapping for simple cases
            return self._create_rule_based_mapping(biztalk_component, best_matches)

    def _find_matches_by_rules(self, biztalk_component: Dict) -> List[Dict]:
        """Rule-based matching to narrow down candidates"""
        biz_type = biztalk_component.get('type', '').lower()
        biz_name = biztalk_component.get('name', '').lower()
        
        matches = []
        
        for ace_comp in self.ace_components:
            ace_patterns = ace_comp.get('technical_patterns', [])
            ace_name = ace_comp.get('name', '').lower()
            
            score = 0
            
            # Type-based matching
            if 'orchestration' in biz_type and 'message' in ace_patterns:
                score += 0.6
            if 'map' in biz_type and 'transformation' in ace_patterns:
                score += 0.7
            if 'schema' in biz_type and ace_comp.get('type') == 'ACE Library':
                score += 0.5
            
            # Name similarity (simple)
            if any(word in ace_name for word in biz_name.split() if len(word) > 3):
                score += 0.3
            
            if score > 0.4:
                matches.append({
                    'ace_component': ace_comp,
                    'score': score,
                    'reasoning': f'Rule-based match (score: {score:.2f})'
                })
        
        # Return top matches
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:3]

    def _create_rule_based_mapping(self, biztalk_component: Dict, matches: List[Dict]) -> Dict:
        """Create mapping using rule-based logic"""
        if not matches:
            return {
                'biztalk_component': biztalk_component.get('name', 'Unknown'),
                'biztalk_component_type': biztalk_component.get('type', 'Unknown'),  # Capture the type
                'ace_matches': [],
                'overall_confidence': 0.2,
                'migration_notes': 'No suitable ACE library found',
                'analysis_method': 'rules'
            }
        
        ace_matches = []
        for match in matches[:2]:  # Top 2 matches
            ace_matches.append({
                'ace_component': match['ace_component'].get('name', 'Unknown'),
                'match_confidence': match['score'],
                'reasoning': match['reasoning']
            })
        
        return {
            'biztalk_component': biztalk_component.get('name', 'Unknown'),
            'biztalk_component_type': biztalk_component.get('type', 'Unknown'),  # Capture the type
            'ace_matches': ace_matches,
            'overall_confidence': matches[0]['score'] if matches else 0.2,
            'migration_notes': 'Rule-based mapping analysis',
            'biztalk_path': biztalk_component.get('path', ''),
            'timestamp': datetime.now().isoformat(),
            'analysis_method': 'rules'
        }

    def _refine_mapping_with_llm(self, biztalk_component: Dict, matches: List[Dict]) -> Optional[Dict]:
        """Use LLM to refine mapping decision among top candidates"""
        if not self.llm_enabled:
            return self._create_rule_based_mapping(biztalk_component, matches)
        
        try:
            # Simple refinement prompt
            candidates = "\n".join([
                f"- {m['ace_component'].get('name', 'Unknown')}: {m['ace_component'].get('business_purpose', 'N/A')}"
                for m in matches[:3]
            ])
            
            prompt = f"""Choose best ACE library for BizTalk component:

BizTalk: {biztalk_component.get('name', 'Unknown')} ({biztalk_component.get('type', 'Unknown')})
Purpose: {biztalk_component.get('purpose', 'Unknown')}

Candidates:
{candidates}

Return JSON:
{{
    "best_match": "exact library name from candidates",
    "confidence": 0.85,
    "reasoning": "brief reason"
}}"""
            
            response = self.llm.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Choose the best ACE library match."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            result = self._parse_json_response(response.choices[0].message.content)
            if result:
                return {
                    'biztalk_component': biztalk_component.get('name', 'Unknown'),
                    'biztalk_component_type': biztalk_component.get('type', 'Unknown'),  # Capture the type
                    'ace_matches': [{
                        'ace_component': result.get('best_match', 'Unknown'),
                        'match_confidence': result.get('confidence', 0.5),
                        'reasoning': result.get('reasoning', 'LLM-refined match')
                    }],
                    'overall_confidence': result.get('confidence', 0.5),
                    'migration_notes': 'LLM-refined mapping decision',
                    'analysis_method': 'hybrid'
                }
            
        except Exception as e:
            self._log(f"⚠️ LLM refinement failed: {e}")
        
        # Fallback to rule-based
        return self._create_rule_based_mapping(biztalk_component, matches)

    def generate_excel(self, output_file: str):
            """Generate Program 2 compatible Excel report at the correct location"""
            self._log("📊 Generating Program 2 compatible Excel report...")

            # DEBUG: Check what's actually in intelligent_mappings
            self._log(f"🔍 DEBUG: Found {len(self.intelligent_mappings)} intelligent mappings")
            for i, mapping in enumerate(self.intelligent_mappings[:3]):  # Show first 3
                biz_name = mapping.get('biztalk_component', '')
                self._log(f"  Mapping {i}: biztalk_component='{biz_name}'")
                self._log(f"  Length of component name: {len(biz_name)} chars")
                if ' ' in biz_name:
                    self._log(f"  ⚠️ ISSUE: Component name contains spaces - indicates concatenation!")
            
            # FIXED: Extract the root directory directly from the output_file path
            # From: C:\@Official\@Gen AI\DSV\BizTalk\Analyze_this_folder\NEW_AI_EPIS_CW1_IN_Document_App\smart_biztalk_ace_mapping.xlsx
            # Get: C:\@Official\@Gen AI\DSV\BizTalk\Analyze_this_folder
            
            output_dir = os.path.dirname(output_file)
            project_name = self._extract_project_name()
            
            # FIXED: Use the output_dir directly as the base directory 
            # This will create folder at: C:\@Official\@Gen AI\DSV\BizTalk\Analyze_this_folder\NEW_AI_MH.ESB.EE.Out.DocPackApp
            structured_output_dir = os.path.join(output_dir, f"NEW_AI_{project_name}")
            
            # Create structured directory
            os.makedirs(structured_output_dir, exist_ok=True)
            
            # Final output file path - directly in the structured directory
            final_output_file = os.path.join(structured_output_dir, "biztalk_ace_mapping.xlsx")
            
            try:
                with pd.ExcelWriter(final_output_file, engine='openpyxl') as writer:
                    
                    # CRITICAL: Component Mapping sheet MUST match Program 2 expectations exactly
                    component_mapping_data = []
                    
                    if self.intelligent_mappings:
                        for mapping in self.intelligent_mappings:
                            # Get BizTalk component info
                            biz_name = mapping.get('biztalk_component', '')
                            biz_type = mapping.get('biztalk_component_type', '')
                            
                            # Get ACE matches
                            ace_matches = mapping.get('ace_matches', [])
                            if ace_matches:
                                for match in ace_matches:
                                    component_mapping_data.append({
                                        'biztalk_component': biz_name,  # Program 2 expects lowercase
                                        'component_type': biz_type,     # Program 2 expects this exact name
                                        'required_ace_library': match.get('ace_component', ''),  # Program 2 expects this exact name
                                        'ace_type': 'ACE Library',
                                        'mapping_confidence': match.get('match_confidence', 0),
                                        'migration_notes': match.get('reasoning', ''),
                                        'analysis_method': mapping.get('analysis_method', 'hybrid')
                                    })
                            else:
                                # Even if no matches, include the component
                                component_mapping_data.append({
                                    'biztalk_component': biz_name,
                                    'component_type': biz_type,
                                    'required_ace_library': 'Manual_Review_Required',  # Default for no mapping
                                    'ace_type': 'Unknown',
                                    'mapping_confidence': 0,
                                    'migration_notes': 'No suitable mapping found',
                                    'analysis_method': mapping.get('analysis_method', 'hybrid')
                                })
                    
                    # Even if no mappings, create empty sheet with proper structure
                    if not component_mapping_data:
                        component_mapping_data = [{
                            'biztalk_component': 'No_Components_Analyzed',
                            'component_type': 'N/A',
                            'required_ace_library': 'Manual_Review_Required',
                            'ace_type': 'N/A',
                            'mapping_confidence': 0,
                            'migration_notes': 'Analysis incomplete',
                            'analysis_method': 'N/A'
                        }]
                    
                    # CRITICAL: Create 'Component Mapping' sheet - Program 2 expects this exact name
                    mapping_df = pd.DataFrame(component_mapping_data)
                    mapping_df.to_excel(writer, sheet_name='Component Mapping', index=False)
                    
                    self._log(f"✅ Created 'Component Mapping' sheet with {len(component_mapping_data)} components")
                    
                    # Summary sheet
                    summary_data = {
                        'migration_summary': [
                            len(self.biztalk_components),
                            len(self.ace_components),
                            len(self.intelligent_mappings),
                            len(self.get_discovered_epis_libraries()),
                            datetime.now().isoformat(),
                            'YES'
                        ]
                    }
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                self._log(f"✅ Program 2 compatible report created: {final_output_file}")
                self._log(f"📁 Directory: {structured_output_dir}")
                self._log(f"📋 Component Mapping sheet: ✅ Created")
                
                return final_output_file
                
            except Exception as e:
                self._log(f"⚠️ Report generation failed: {e}")
                raise

    def _extract_project_name(self) -> str:
        """Extract project name for folder naming"""
        # Try to extract project name from BizTalk components
        for comp in self.biztalk_components:
            if comp.get('type') == 'BizTalk Project' or 'project' in comp.get('type', '').lower():
                return comp.get('name', 'EPIS_CW1_IN_Document_App')
        
        # Fallback to default naming pattern
        return "EPIS_CW1_IN_Document_App"

    def run_full_analysis(self, biztalk_path: str, ace_path: str, output_file: str) -> str:
        """Run complete hybrid analysis with Program 2 compatible output"""
        self._log("🚀 Starting Hybrid BizTalk to ACE Analysis")
        
        try:
            # Hybrid analysis
            self.scan_biztalk(biztalk_path)
            self.scan_ace_libraries(ace_path)
            self.create_mappings()
            
            # Generate Program 2 compatible report and folder structure
            os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
            final_output_file = self.generate_excel(output_file)  # This now returns the actual file path
            
            # Final statistics
            self._log("🎯 Hybrid Analysis Complete")
            self._log(f"   • BizTalk Components: {len(self.biztalk_components)}")
            self._log(f"   • ACE Libraries: {len(self.ace_components)}")  
            self._log(f"   • Intelligent Mappings: {len(self.intelligent_mappings)}")
            
            llm_analyzed = len([c for c in self.biztalk_components if c.get('analysis_method') == 'llm'])
            self._log(f"   • LLM Analyzed: {llm_analyzed}")
            self._log(f"   • Rule Analyzed: {len(self.biztalk_components) - llm_analyzed}")
            
            epis_count = len(self.get_discovered_epis_libraries())
            self._log(f"   • EPIS Libraries: {epis_count}")
            self._log(f"📁 Program 2 Ready: {final_output_file}")
            
            return final_output_file  # Return the actual generated file path
            
        except Exception as e:
            self._log(f"❌ Hybrid analysis failed: {e}")
            raise

    # Legacy property accessors for main.py compatibility - ENHANCED
    @property  
    def results(self):
        """Legacy results property for main.py compatibility"""
        return {
            "biztalk": self.biztalk_components,
            "ace": self.ace_components, 
            "mappings": self.intelligent_mappings
        }
    
    def get_all_discovered_libraries(self):
        """Legacy method for main.py compatibility"""
        return [comp.get('name', 'Unknown') for comp in self.ace_components]
    
    def get_discovered_epis_libraries(self):
        """Legacy method for main.py compatibility"""
        epis_libraries = []
        for comp in self.ace_components:
            comp_name = comp.get('name', '').lower()
            if 'epis' in comp_name:
                epis_libraries.append(comp.get('name', 'Unknown'))
        return epis_libraries

    def _calculate_overall_score(self):
        """Calculate overall analysis quality score for compatibility"""
        if not self.intelligent_mappings:
            return 0
        
        total_confidence = sum(mapping.get('overall_confidence', 0) for mapping in self.intelligent_mappings)
        average_confidence = total_confidence / len(self.intelligent_mappings)
        return int(average_confidence * 100)  # Convert to percentage


# Main execution
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Hybrid Smart BizTalk to ACE Mapper')
    parser.add_argument('--biztalk_path', required=True, help='BizTalk components path')
    parser.add_argument('--ace_path', required=True, help='ACE libraries path')
    parser.add_argument('--output', default='hybrid_mapping.xlsx', help='Output file')
    
    args = parser.parse_args()
    
    # Validate paths
    if not os.path.exists(args.biztalk_path):
        print(f"❌ BizTalk path not found: {args.biztalk_path}")
        exit(1)
    
    if not os.path.exists(args.ace_path):
        print(f"❌ ACE path not found: {args.ace_path}")
        exit(1)
    
    print("🚀 Hybrid Smart BizTalk to ACE Mapper")
    print("   LLM for .project files + Rules for .esql files")
    print("   Fast, Reliable, and Intelligent")
    print("=" * 60)
    
    # Run hybrid analysis
    mapper = SmartBizTalkMapper()
    
    try:
        result_file = mapper.run_full_analysis(
            biztalk_path=args.biztalk_path,
            ace_path=args.ace_path,
            output_file=args.output
        )
        
        print("=" * 60)
        print("✅ Hybrid mapping completed successfully!")
        print(f"📊 Results: {result_file}")
        print("🎯 Analysis Methods Used:")
        
        llm_count = len([c for c in mapper.biztalk_components if c.get('analysis_method') == 'llm'])
        rule_count = len(mapper.biztalk_components) - llm_count
        
        print(f"   • LLM Analysis: {llm_count} components")
        print(f"   • Rule Analysis: {rule_count} components")
        print(f"   • Hybrid Libraries: {len(mapper.ace_components)} libraries")
        
        avg_confidence = sum(m.get('overall_confidence', 0) for m in mapper.intelligent_mappings) / max(len(mapper.intelligent_mappings), 1)
        print(f"   • Average Mapping Confidence: {avg_confidence:.2f}")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Hybrid mapping failed: {e}")
        print("Check logs for detailed error information")
        exit(1)