#!/usr/bin/env python3
"""
Enhanced Prompt Module for ACE Generation
Updated to handle MessageFlow templates and enforce ESQL coding standards
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class PromptModule:
    """Enhanced prompt generation for ACE components with strict ESQL rules"""
    
    def __init__(self):
        self.system_context = """You are an expert IBM ACE (App Connect Enterprise) developer with deep knowledge of:
- MessageFlow XML structure and node configurations
- ESQL programming best practices and syntax
- IBM ACE runtime behavior and performance optimization
- BizTalk to ACE migration patterns
- Database integration and message transformation patterns"""

    def get_system_context(self) -> str:
        """Get the system context for LLM prompts"""
        return self.system_context


def get_msgflow_generation_prompt(flow_name: str, project_name: str, 
                                input_queue: str, output_service: str, error_queue: str,
                                esql_modules: List[Dict], msgflow_template: str = None,
                                confluence_spec: str = None, components_info: List[Dict] = None) -> str:
    """
    Generate comprehensive MessageFlow creation prompt using provided template
    
    Args:
        flow_name: Name of the message flow
        project_name: Name of the ACE project
        input_queue: Input queue name
        output_service: Output service endpoint
        error_queue: Error queue name
        esql_modules: List of ESQL modules to integrate
        msgflow_template: MessageFlow XML template to use as base
        confluence_spec: Business specification document
        components_info: BizTalk component information
    """
    
    prompt = f"""# IBM ACE MessageFlow Generation Task

You are an expert IBM ACE developer. Generate a production-ready MessageFlow XML based on the provided template and specifications.

## TEMPLATE PROVIDED:
```xml
{msgflow_template if msgflow_template else "No template provided - create from scratch"}
```

## BUSINESS REQUIREMENTS (from Confluence):
```
{confluence_spec[:1500] if confluence_spec else "No specification provided"}
```

## COMPONENT MAPPING CONTEXT:
"""
    
    if components_info:
        for comp in components_info[:5]:  # Limit to first 5 components
            prompt += f"""
- **{comp.get('biztalk_component', 'Unknown')}**: {comp.get('component_type', 'Unknown')} → {comp.get('ace_library', 'Unknown')}"""
    
    prompt += f"""

## MESSAGEFLOW SPECIFICATIONS:
- **Flow Name**: {flow_name}
- **Project**: {project_name}
- **Input Queue**: {input_queue}
- **Output Service**: {output_service}
- **Error Queue**: {error_queue}

## ESQL MODULES TO INTEGRATE:
"""
    
    for module in esql_modules:
        prompt += f"""
- **{module.get('name', 'Unknown')}**: {module.get('purpose', 'Processing')}"""
    
    prompt += f"""

## GENERATION REQUIREMENTS:

### 1. XML Structure Requirements (CRITICAL):
- Use the provided template as the EXACT foundation structure
- Maintain ALL namespace declarations (xmlns) exactly as in template
- Preserve node positioning and connection patterns from template
- Update ONLY node names, properties, and connections based on requirements
- DO NOT modify the root element structure or namespace URIs

### 2. Node Configuration:
- Configure MQInput node for queue: {input_queue}
- Configure HTTPRequest/SOAPRequest for service: {output_service}
- Configure MQOutput node for error queue: {error_queue}
- Add Compute nodes for each ESQL module integration
- Include proper error handling with TryCatch nodes
- Use node IDs following template pattern (e.g., FCMComposite_1_1, FCMComposite_1_2)

### 3. Flow Logic Requirements:
- Implement message validation at entry point
- Add database enrichment nodes based on specification
- Include transformation logic based on BizTalk component mapping
- Implement proper error handling and logging
- Add audit trail and monitoring capabilities
- Connect all nodes following template terminal patterns

### 4. Production Standards:
- Include comprehensive error handling
- Add proper message correlation
- Implement timeout and retry mechanisms  
- Include security and authentication nodes if required
- Follow IBM ACE best practices for performance

### 5. MANDATORY XML Structure Elements:
- Ensure <propertyOrganizer/> is added AFTER </composition> closing tag
- Ensure <stickyBoard/> is added AFTER </composition> closing tag
- These elements are REQUIRED for proper IBM ACE Toolkit compatibility

### 6. MANDATORY Graphic Resources (BEFORE <composition>):
Add these graphic resource declarations BEFORE the <composition> element:
```xml
<colorGraphic16 xmi:type="utility:GIFFileGraphic" resourceName="platform:/plugin/{self.app_name}/icons/full/obj16/{self.flow_name}.gif"/>
<colorGraphic32 xmi:type="utility:GIFFileGraphic" resourceName="platform:/plugin/{self.app_name}/icons/full/obj30/{self.flow_name}.gif"/>
```

### 7. XML Validation Rules:
- Ensure ALL opening tags have matching closing tags
- Verify all node references in connections exist
- Check that all xmi:id values are unique
- Validate that terminal references match actual terminal names
- Ensure proper XML escaping for special characters

### 8. Connection Requirements:
- Every node MUST have proper input/output terminal connections
- Follow the connection pattern: sourceNode.terminalName to targetNode.terminalName
- Ensure all connections reference valid xmi:id values
- Include failure terminals for error handling paths

## CRITICAL ERROR PREVENTION:
- DO NOT create nodes with types not present in the template
- DO NOT modify namespace URLs (xmlns values)
- DO NOT change the basic FCMComposite structure
- DO NOT add unsupported properties to nodes
- DO NOT create orphaned nodes without connections

## OUTPUT REQUIREMENTS:
- Generate ONLY the complete MessageFlow XML content
- Do not include explanations or comments outside the XML
- Ensure valid XML syntax with proper namespaces
- Test that all node references are properly connected
- Include proper XML declaration at the top
- End with proper closing tags for all elements

## XML OUTPUT FORMAT:
Provide the complete, production-ready MessageFlow XML below:

```xml"""
    
    return prompt


def get_esql_creation_prompt(module_name: str, purpose: str, business_context: str = None,
                           additional_context: Dict[str, Any] = None) -> str:
    """
    Generate ESQL module creation prompt with strict coding standards
    
    Args:
        module_name: Name of the ESQL module
        purpose: Purpose/functionality of the module
        business_context: Business requirements context
        additional_context: Additional context information
    """
    
    prompt = f"""# IBM ACE ESQL Module Generation

Create a production-ready ESQL module for IBM ACE with the following specifications:

## MODULE DETAILS:
- **Module Name**: {module_name}
- **Purpose**: {purpose}
- **Generated**: {datetime.now().isoformat()}

## BUSINESS CONTEXT:
```
{business_context[:1000] if business_context else "Standard transformation module"}
```
"""
    
    if additional_context:
        prompt += f"""
## MIGRATION CONTEXT:
- **Source BizTalk Component**: {additional_context.get('biztalk_source', 'Unknown')}
- **Component Type**: {additional_context.get('component_type', 'Unknown')}
- **Target ACE Library**: {additional_context.get('target_ace_library', 'Unknown')}
"""
    
    prompt += f"""

## CRITICAL ESQL CODING RULES - MUST FOLLOW:

### 🚫 FORBIDDEN ELEMENTS:
1. **NEVER start any line with "esql"** - this is strictly forbidden
2. **NEVER use "@" symbol anywhere in the code** - not allowed in ESQL
3. **NEVER use "```esql"** markers - generate pure ESQL code only
4. **NEVER include language identifiers** in the code

### ✅ REQUIRED ESQL STRUCTURE:
```
CREATE COMPUTE MODULE {module_name}_Compute
    CREATE FUNCTION Main() RETURNS BOOLEAN
    BEGIN
        -- Your implementation here
        RETURN TRUE;
    END;
END MODULE;

CREATE PROCEDURE ProcedureName()
BEGIN
    -- Procedure implementation
END;
```

### ✅ MANDATORY ESQL PATTERNS:

#### Database Operations:
```
DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
    SET Environment.Variables.LastSQLError = SQLERRORTEXT;
    PROPAGATE TO TERMINAL 'failure';
END;

SET DATABASE.param1 = InputRoot.XMLNSC.Element;
```

#### Message Processing:
```
SET OutputRoot = InputRoot;
SET OutputRoot.MQMD.MsgId = UUIDASBLOB();
SET OutputRoot.XMLNSC.ElementName = COALESCE(InputRoot.XMLNSC.ElementName, 'default');
```

#### Error Handling:
```
IF COALESCE(fieldValue,'') = '' THEN
    SET Environment.Variables.ValidationError = 'Field required';
    PROPAGATE TO TERMINAL 'failure';
END IF;
```

## IMPLEMENTATION REQUIREMENTS:

### 1. Core Functionality:
- Implement the {purpose} logic
- Include proper message copying and manipulation
- Add validation for required fields
- Implement error handling with meaningful messages

### 2. Database Integration (if applicable):
- Use parameterized queries with SET DATABASE syntax
- Include proper connection error handling
- Add retry logic for transient failures
- Log all database operations

### 3. Message Structure:
- Copy InputRoot to OutputRoot as starting point
- Generate new message IDs using UUIDASBLOB()
- Preserve correlation IDs for tracking
- Handle both XML and JSON message formats

### 4. Performance Optimization:
- Use COALESCE for safe field access
- Minimize XPath expressions
- Cache frequently accessed values
- Implement efficient looping patterns

### 5. Production Standards:
- Include comprehensive error handling
- Add audit logging capabilities
- Implement proper validation
- Follow IBM ACE naming conventions

## OUTPUT REQUIREMENTS:
- Generate ONLY pure ESQL code
- Start directly with CREATE statements
- No code block markers or language tags
- No "@" symbols anywhere in the code
- No lines starting with "esql"
- Complete, runnable ESQL module

## ESQL MODULE CODE:
Generate the complete ESQL module below:

"""
    
    return prompt


def get_enhancement_prompt(original_esql: str, enhancement_type: str, context: Dict = None) -> str:
    """Generate prompt for enhancing existing ESQL code"""
    
    prompt = f"""# ESQL Module Enhancement Task

Enhance the following ESQL module with {enhancement_type} capabilities:

## ORIGINAL ESQL CODE:
```
{original_esql}
```

## ENHANCEMENT TYPE: {enhancement_type}

## CRITICAL ESQL RULES - MUST FOLLOW:
1. **NEVER start any line with "esql"**
2. **NEVER use "@" symbol anywhere**
3. **NEVER include code block markers**
4. **Generate pure ESQL code only**

## ENHANCEMENT REQUIREMENTS:
"""
    
    if enhancement_type == "database_operations":
        prompt += """
### Database Enhancement:
- Add robust database lookup procedures
- Implement connection pooling and error handling
- Add retry logic for transient failures
- Use parameterized queries for security
- Include audit logging for all database operations

### Required Database Pattern:
```
DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
    SET Environment.Variables.LastSQLError = SQLERRORTEXT;
    PROPAGATE TO TERMINAL 'failure';
END;

SET DATABASE.CompanyCode = InputRoot.XMLNSC.Header.CompanyCode;
SET CompanyName = THE(SELECT ITEM C.CompanyName FROM Database.Companies AS C WHERE C.CompanyCode = DATABASE.CompanyCode);
```
"""
    
    elif enhancement_type == "business_logic":
        prompt += """
### Business Logic Enhancement:
- Implement complex business rules and validations
- Add decision trees for routing logic
- Include data enrichment and transformation
- Add proper field validation and error messages
"""
    
    elif enhancement_type == "error_handling":
        prompt += """
### Error Handling Enhancement:
- Implement comprehensive try/catch patterns
- Add specific error codes and messages
- Include proper error logging and auditing
- Add error recovery mechanisms
"""
    
    prompt += f"""

## CONTEXT INFORMATION:
{json.dumps(context, indent=2) if context else "No additional context provided"}

## OUTPUT REQUIREMENTS:
- Enhance the original ESQL with the requested capabilities
- Maintain all existing functionality
- Follow IBM ACE best practices
- Generate complete, production-ready ESQL module
- No code block markers or language identifiers

## ENHANCED ESQL MODULE:
"""
    
    return prompt


def get_quality_analysis_prompt(esql_code: str) -> str:
    """Generate prompt for ESQL quality analysis"""
    
    return f"""# ESQL Code Quality Analysis

Analyze the following ESQL code for quality, performance, and best practices:

## ESQL CODE TO ANALYZE:
```
{esql_code}
```

## ANALYSIS CRITERIA:
1. **Code Quality**: Syntax, structure, readability
2. **Performance**: Efficiency, optimization opportunities
3. **Best Practices**: IBM ACE standards compliance
4. **Error Handling**: Robustness and error coverage
5. **Security**: Input validation and SQL injection protection
6. **Maintainability**: Code organization and documentation

## FORBIDDEN ELEMENTS CHECK:
- Verify no lines start with "esql"
- Verify no "@" symbols are used
- Verify proper ESQL syntax throughout

## PROVIDE ANALYSIS:
1. **Quality Score**: Rate from 1-100
2. **Issues Found**: List any problems or violations
3. **Improvements**: Specific recommendations
4. **Best Practices**: Adherence to IBM ACE standards

## ANALYSIS RESULT:
"""


# Utility functions for prompt management
def save_prompt_to_file(prompt: str, filename: str) -> str:
    """Save generated prompt to file for reference"""
    import os
    os.makedirs("prompts", exist_ok=True)
    filepath = os.path.join("prompts", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(prompt)
    return filepath


def load_template(template_name: str) -> str:
    """Load prompt template from file"""
    try:
        with open(f"templates/{template_name}.txt", 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Template {template_name} not found"


def get_functional_documentation_prompt(biztalk_analysis: Dict, confluence_analysis: Dict = None) -> str:
    """
    Generate prompt for creating functional requirements documentation
    
    Args:
        biztalk_analysis: Analysis results from BizTalk scanning
        confluence_analysis: Optional confluence specification analysis
    """
    
    prompt = f"""# Functional Requirements Document Generation

You are a business analyst expert in BizTalk to IBM ACE migration. Generate a comprehensive functional requirements document.

## BIZTALK ANALYSIS DATA:
```json
{json.dumps(biztalk_analysis, indent=2)[:2000]}
```

## BUSINESS SPECIFICATION:
```
{json.dumps(confluence_analysis, indent=2)[:1500] if confluence_analysis else "No business specification provided"}
```

## DOCUMENT REQUIREMENTS:

### 1. Executive Summary
- Purpose and scope of the migration
- High-level business benefits
- Key stakeholders and impact areas

### 2. Current State Analysis
- BizTalk architecture overview
- Component inventory and dependencies
- Integration points and data flows
- Business processes supported

### 3. Future State Design
- IBM ACE target architecture
- Component mapping strategy
- New capabilities and improvements
- Integration patterns in ACE

### 4. Functional Requirements
- Business process requirements
- Data transformation requirements
- Integration requirements
- Performance and scalability requirements
- Security and compliance requirements

### 5. Migration Strategy
- Component migration approach
- Testing strategy
- Deployment approach
- Risk mitigation
- Timeline and milestones

### 6. Technical Specifications
- ACE component specifications
- ESQL module requirements
- Message flow definitions
- Schema and data model requirements

## OUTPUT FORMAT:
Generate a comprehensive markdown document with:
- Clear section headers using # and ##
- Bullet points for lists and requirements
- Tables for component mappings where appropriate
- Professional business language
- Technical accuracy for IBM ACE
- Actionable recommendations

## FUNCTIONAL REQUIREMENTS DOCUMENT:
"""
    
    return prompt


# Configuration for different prompt types
PROMPT_CONFIG = {
    "msgflow": {
        "max_template_size": 5000,
        "max_spec_size": 2000,
        "include_business_context": True
    },
    "esql": {
        "max_context_size": 1500,
        "enforce_coding_rules": True,
        "include_error_handling": True
    },
    "enhancement": {
        "preserve_existing_logic": True,
        "add_production_features": True
    },
    "documentation": {
        "max_analysis_size": 2000,
        "include_technical_details": True,
        "business_focus": True
    }
}