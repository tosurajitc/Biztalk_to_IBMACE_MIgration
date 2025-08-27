#!/usr/bin/env python3
"""
Streamlit Main UI - BizTalk to ACE Migration Pipeline
Complete UI for all 5 programs with progress tracking
MINIMAL UPDATE: Only adds Program 5 tab, preserves all existing functionality
"""

import streamlit as st
import os
import sys
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import traceback


# Import our migration programs
try:
    from biztalk_ace_mapper import SmartBizTalkMapper
    from messageflow_generator import StreamlinedACEGenerator  
    from migration_quality_reviewer import MigrationQualityReviewer
    from functional_document_generator import FunctionalDocumentGenerator  # NEW IMPORT ONLY
    PROGRAMS_AVAILABLE = True
except ImportError as e:
    PROGRAMS_AVAILABLE = False
    st.error(f"❌ Migration programs not found: {e}")

# Page configuration
st.set_page_config(
    page_title="BizTalk to ACE Migration",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🔄 BizTalk to IBM ACE Migration Pipeline")
    st.markdown("**Automated migration with AI-powered enhancement and documentation**")  # MINOR UPDATE
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("📋 Migration Pipeline")
        
        # Environment selector
        environment = st.selectbox(
            "Environment", 
            ["POC (Local)", "MVP (Connected)"],
            help="POC uses local folders, MVP connects to external systems"
        )
        
        # Pipeline status
        st.subheader("🚀 Pipeline Status")
        
        # Initialize session state for progress tracking
        if 'pipeline_progress' not in st.session_state:
            st.session_state.pipeline_progress = {
                'program_1': {'status': 'pending', 'output': None},
                'program_2': {'status': 'pending', 'output': None},
                'program_3': {'status': 'pending', 'output': None},
                'program_4': {'status': 'pending', 'output': None},
                'program_5': {'status': 'pending', 'output': None}  # NEW PROGRAM 5 ONLY
            }
        
        # Display pipeline progress
        progress = st.session_state.pipeline_progress
        
        st.write("**Program 1**: BizTalk Mapper", get_status_icon(progress['program_1']['status']))
        st.write("**Program 2**: ACE Foundation", get_status_icon(progress['program_2']['status']))
        st.write("**Program 3**: LLM Enhancement", get_status_icon(progress['program_3']['status']))
        st.write("**Program 4**: Quality Review", get_status_icon(progress['program_4']['status']))
        st.write("**Program 5**: Functional Docs", get_status_icon(progress['program_5']['status']))  # NEW LINE ONLY
        
        # Reset pipeline button
        if st.button("🔄 Reset Pipeline"):
            reset_pipeline()
            st.rerun()
    
    # Main content area
    if not PROGRAMS_AVAILABLE:
        st.error("❌ Migration programs not available. Please ensure all Python files are in the same directory.")
        return
    
    # Create tabs for each program - UPDATED TO ADD PROGRAM 5 TAB
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📁 Agent 1: Mapping", 
        "🏗️ Agent 2: Messageflow", 
        "🧠 Agent 3: Foundation", 
        "🔍 Agent 4: Quality", 
        "📋 Agent 5: Postman",  
    ])
    
    with tab1:
        render_program_1_ui(environment)
    
    with tab2:
        render_program_2_ui()
    
    with tab3:
        render_program_3_ui()
    
    with tab4:
        render_program_4_ui()
    
    with tab5:  # NEW TAB CONTENT ONLY
        render_program_5_ui()
    



# ALL EXISTING FUNCTIONS BELOW - COMPLETELY UNCHANGED

def get_status_icon(status):
    """Get status icon for pipeline progress"""
    icons = {
        'pending': '⏳',
        'running': '🔄',
        'success': '✅',
        'error': '❌'
    }
    return icons.get(status, '❓')

def reset_pipeline():
    """Reset pipeline progress"""
    st.session_state.pipeline_progress = {
        'program_1': {'status': 'pending', 'output': None},
        'program_2': {'status': 'pending', 'output': None},
        'program_3': {'status': 'pending', 'output': None},
        'program_4': {'status': 'pending', 'output': None},
        'program_5': {'status': 'pending', 'output': None}  # UPDATED TO INCLUDE PROGRAM 5
    }

def render_program_1_ui(environment):
    """Render Program 1: BizTalk ACE Mapper UI with GROQ API Key"""
    st.header("🔍 Agent 1: Smart BizTalk to ACE Mapper")
    st.markdown("LLM-powered intelligent component analysis and mapping - **NO rule-based fallbacks**")
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📂 BizTalk Source")
            if environment == "POC (Local)":
                biztalk_path = st.text_input(
                    "BizTalk Projects Folder",
                    value=r"C:\@Official\@Gen AI\DSV\BizTalk\MH.ESB.EE.Out.DocPackApp\MH.ESB.EE.Out.DocPackApp",
                    help="Path to your BizTalk source folder"
                )
            else:
                st.info("🔮 MVP: Will connect to TFS/Azure DevOps")
                biztalk_path = st.text_input("TFS Workspace URL", placeholder="https://dev.azure.com/...")
        
        with col2:
            st.subheader("📚 ACE Libraries")
            if environment == "POC (Local)":
                ace_path = st.text_input(
                    "ACE Libraries Folder",
                    value=r"C:\@Official\@Gen AI\DSV\BizTalk\Analyze_this_folder\libraries",
                    help="Path to your ACE libraries folder"
                )
            else:
                st.info("🔮 MVP: Will connect to ACE Workspace")
                ace_path = st.text_input("ACE Workspace URL", placeholder="https://ace-workspace...")

    # LLM Configuration - NEW SECTION
    with st.expander("🤖 LLM Intelligence Configuration", expanded=True):
        st.markdown("**Required**: This program uses LLM reasoning for intelligent component mapping")
        
        col1, col2 = st.columns(2)
        
        with col1:
            groq_api_key = st.text_input(
                "GROQ API Key", 
                value=os.getenv('GROQ_API_KEY', ''), 
                type="password",
                help="Get your API key from https://console.groq.com/"
            )
            
            groq_model = st.selectbox(
                "LLM Model",
                ["llama3-70b-8192", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
                help="Choose the AI model for component analysis"
            )
        
        with col2:
            llm_temperature = st.slider(
                "Analysis Precision", 
                min_value=0.0, 
                max_value=0.5, 
                value=0.1,
                help="0.0 = Most precise, 0.5 = More creative analysis"
            )
            
            confidence_threshold = st.slider(
                "Mapping Confidence Threshold",
                min_value=0.5,
                max_value=1.0,
                value=0.7,
                help="Minimum confidence score for accepting mappings"
            )

    # Advanced Configuration
    with st.expander("⚙️ Advanced Configuration"):
        col1, col2 = st.columns(2)
        
        with col1:
            file_extensions = st.multiselect(
                "BizTalk File Types",
                [".odx", ".btm", ".xsd", ".btp", ".btproj", ".cs", ".dll", ".config"],
                default=[".odx", ".btm", ".xsd", ".btp", ".btproj"],
                help="File extensions to analyze"
            )
        
        with col2:
            output_dir = st.text_input(
                "Output Directory",
                value="GENAI_ACE",
                help="Directory for generated reports"
            )

    # Validation
    missing_inputs = []
    if not biztalk_path:
        missing_inputs.append("BizTalk path")
    if not ace_path:
        missing_inputs.append("ACE libraries path")
    if not groq_api_key:
        missing_inputs.append("GROQ API Key")

    if missing_inputs:
        st.error(f"🔑 Required: {', '.join(missing_inputs)}")
        return

    # Path validation
    if environment == "POC (Local)":
        if not os.path.exists(biztalk_path):
            st.error(f"❌ BizTalk path not found: {biztalk_path}")
            return
        if not os.path.exists(ace_path):
            st.error(f"❌ ACE libraries path not found: {ace_path}")
            return

    # Execute button
    if st.button("🧠 Run Smart LLM Analysis", type="primary", key="run_prog1"):
        run_program_1(biztalk_path, ace_path, output_dir, file_extensions, groq_api_key, groq_model, llm_temperature, confidence_threshold)


def run_program_1(biztalk_path, ace_path, output_dir, file_extensions, groq_api_key, groq_model, temperature, confidence_threshold):
    """Execute Program 1 with LLM configuration"""
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    try:
        # Update status
        st.session_state.pipeline_progress['program_1']['status'] = 'running'
        progress_placeholder.progress(0)
        status_placeholder.info("🔄 Initializing Smart LLM Mapper...")
        
        # Set GROQ environment variable
        os.environ['GROQ_API_KEY'] = groq_api_key
        
        # Initialize mapper
        mapper = SmartBizTalkMapper()
        
        # Configure LLM settings
        mapper.model = groq_model
        mapper.temperature = temperature
        
        def progress_callback(message):
            status_placeholder.info(f"🔄 {message}")
        
        mapper.set_progress_callback(progress_callback)
        
        # Execute LLM-powered analysis
        progress_placeholder.progress(20)
        mapper.scan_biztalk(biztalk_path, file_extensions)
        mapper.scan_biztalk(biztalk_path, file_extensions)

        # DEBUG: Check what components were actually found
        print("DEBUG - First few biztalk_components:")
        for i, comp in enumerate(mapper.biztalk_components[:3]):
            print(f"  {i}: name='{comp.get('name')}', file_name='{comp.get('file_name')}', type='{comp.get('type')}'")
        
        progress_placeholder.progress(50)
        mapper.scan_ace_libraries(ace_path)
        
        progress_placeholder.progress(75)
        mapper.create_mappings()
        
        # Generate output
        output_file = os.path.join(output_dir, "smart_biztalk_ace_mapping.xlsx")
        actual_output_file = mapper.generate_excel(output_file)
        
        progress_placeholder.progress(100)
        
        # Update session state
        st.session_state.pipeline_progress['program_1']['status'] = 'success'
        st.session_state.pipeline_progress['program_1']['output'] = actual_output_file
        
        # Show results with LLM insights
        status_placeholder.success(f"✅ Smart LLM Analysis completed!")
        
        # Display intelligent analysis results
        st.subheader("🧠 LLM Analysis Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("BizTalk Components", len(mapper.biztalk_components))
            st.metric("ACE Components", len(mapper.ace_components))
        
        with col2:
            st.metric("Intelligent Mappings", len(mapper.intelligent_mappings))
            high_confidence = len([m for m in mapper.intelligent_mappings if m.get('overall_confidence', 0) > confidence_threshold])
            st.metric("High Confidence Mappings", high_confidence)
        
        with col3:
            avg_confidence = sum(m.get('overall_confidence', 0) for m in mapper.intelligent_mappings) / max(len(mapper.intelligent_mappings), 1)
            st.metric("Average Confidence", f"{avg_confidence:.2f}")
            complex_migrations = len([m for m in mapper.intelligent_mappings if m.get('migration_complexity') == 'HIGH'])
            st.metric("Complex Migrations", complex_migrations)

        # Show sample intelligent mappings
        if mapper.intelligent_mappings:
            st.subheader("🎯 Sample Intelligent Mappings")
            sample_mappings = mapper.intelligent_mappings[:3]  # Show first 3
            
            for mapping in sample_mappings:
                with st.expander(f"📋 {mapping.get('biztalk_component', 'Unknown')} → ACE Components"):
                    st.write(f"**Confidence:** {mapping.get('overall_confidence', 0):.2f}")
                    st.write(f"**Complexity:** {mapping.get('migration_complexity', 'Unknown')}")
                    
                    ace_matches = mapping.get('ace_matches', [])
                    if ace_matches:
                        st.write("**Recommended ACE Components:**")
                        for match in ace_matches:
                            st.write(f"• {match.get('ace_component', 'Unknown')} (Confidence: {match.get('match_confidence', 0):.2f})")
                            if match.get('reasoning'):
                                st.write(f"  *Reasoning: {match.get('reasoning', 'No reasoning provided')}*")

        # Download button
        with open(actual_output_file, "rb") as file:
            st.download_button(
                label="📊 Download Smart Mapping Report",
                data=file.read(),
                file_name="smart_biztalk_ace_mapping.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
    except Exception as e:
        st.session_state.pipeline_progress['program_1']['status'] = 'error'
        error_msg = str(e)
        status_placeholder.error(f"❌ Program 1 failed: {error_msg}")
        
        # Show specific error guidance
        if "GROQ_API_KEY" in error_msg:
            st.error("🔑 GROQ API Key is required for LLM analysis. Please enter a valid API key.")
        elif "connection" in error_msg.lower():
            st.error("🌐 Network connection issue. Please check your internet connection and try again.")
        else:
            st.error(f"Error details: {error_msg}")
            
        # Show error details in expander
        with st.expander("🔍 Full Error Details"):
            import traceback
            st.code(traceback.format_exc())

            

def preview_program_1(biztalk_path, ace_path):
    """Preview Program 1 analysis"""
    with st.spinner("🔍 Previewing analysis..."):
        try:
            if os.path.exists(biztalk_path):
                biztalk_files = list(Path(biztalk_path).rglob("*"))
                st.info(f"📁 BizTalk: Found {len(biztalk_files)} files")
            
            if os.path.exists(ace_path):
                ace_files = list(Path(ace_path).rglob("*"))
                st.info(f"📚 ACE: Found {len(ace_files)} files")
        except Exception as e:
            st.error(f"Preview failed: {e}")


def render_program_2_ui():
    """Render Program 2: MessageFlow Generator UI - Streamlined for MessageFlow Only"""
    st.header("🎯 Agent 2: MessageFlow Generator")
    st.markdown("**Focus**: Generate enterprise-ready ACE MessageFlow using BizTalk transformation logic")
    
    # Validate backend availability
    try:
        from messageflow_generator import StreamlinedACEGenerator, run_messageflow_generator
        st.success("✅ MessageFlow Generator ready")
    except ImportError as e:
        st.error(f"❌ MessageFlow Generator not available: {e}")
        st.error("Ensure messageflow_generator.py is available")
        return
    
    # Check Program 1 completion
    prog1_status = st.session_state.pipeline_progress['program_1']['status']
    if prog1_status != 'success':
        st.warning("⚠️ Program 1 must be completed first to get component mappings")
        return
    
    # Show Program 1 output
    mapping_file = st.session_state.pipeline_progress['program_1']['output']
    st.info(f"📊 **Component Mappings**: {os.path.basename(mapping_file)}")
    
    # Preview component data
    try:
        component_df = pd.read_excel(mapping_file, sheet_name='Component Mapping')
        st.info(f"📋 Ready to process {len(component_df)} components")
    except Exception as e:
        st.error(f"❌ Cannot read component mappings: {e}")
        return
    
    st.markdown("---")
    
    # Required Inputs Section
    st.subheader("📋 Required Inputs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**1. MessageFlow Template**")
        msgflow_template = st.file_uploader(
            "Upload MessageFlow XML Template",
            type=['xml'],
            key="msgflow_template_p2",
            help="ACE MessageFlow template for structure reference"
        )
        
        if msgflow_template:
            st.success(f"✅ Template: {msgflow_template.name}")
            with st.expander("🔍 Preview Template"):
                content = msgflow_template.read().decode('utf-8')
                st.code(content[:800] + "..." if len(content) > 800 else content, language='xml')
                msgflow_template.seek(0)
    
    with col2:
        st.markdown("**2. Business Requirements**")
        confluence_doc = st.file_uploader(
            "Upload Confluence Document",
            type=['pdf', 'html', 'htm', 'docx', 'txt', 'md'],
            key="confluence_doc_p2",
            help="Business requirements and specifications"
        )
        
        if confluence_doc:
            st.success(f"✅ Document: {confluence_doc.name}")
            st.info(f"📄 Size: {len(confluence_doc.read())/1024:.1f} KB")
            confluence_doc.seek(0)
    
    # BizTalk Maps Path
    st.markdown("**3. BizTalk Maps Path**")
    biztalk_maps_path = st.text_input(
        "Path to BizTalk .btm files",
        value=r"C:\@Official\@Gen AI\DSV\BizTalk\MH.ESB.EE.Out.DocPackApp\MH.ESB.EE.Out.DocPackApp\MH.ESB.EE.Out.DocPackApp\Maps",
        help="Folder containing BizTalk Map (.btm) files for transformation logic"
    )
    
    # Validate BizTalk path
    if biztalk_maps_path:
        if os.path.exists(biztalk_maps_path):
            from pathlib import Path
            btm_files = list(Path(biztalk_maps_path).glob("*.btm"))
            if btm_files:
                st.success(f"✅ Found {len(btm_files)} .btm files in path")
                with st.expander("📁 BizTalk Maps Found"):
                    for btm_file in btm_files[:10]:  # Show first 10
                        st.text(f"• {btm_file.name}")
                    if len(btm_files) > 10:
                        st.text(f"... and {len(btm_files) - 10} more files")
            else:
                st.warning(f"⚠️ No .btm files found in: {biztalk_maps_path}")
        else:
            st.error(f"❌ Path does not exist: {biztalk_maps_path}")
    
    # LLM Configuration
    st.subheader("🤖 LLM Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        app_name = st.text_input(
            "ACE Application Name", 
            value="EPIS_MessageFlow_App",
            help="Name for the generated ACE application"
        )
        
        flow_name = st.text_input(
            "MessageFlow Name", 
            value="Enterprise_MessageFlow",
            help="Name for the generated MessageFlow"
        )
    
    with col2:
        groq_api_key = st.text_input(
            "GROQ API Key", 
            type="password",
            value=os.getenv('GROQ_API_KEY', ''),
            help="Required for LLM processing"
        )
        
        groq_model = st.selectbox(
            "GROQ Model", 
            ["llama3-70b-8192", "llama-3.3-70b-versatile"],
            index=1,
            help="AI model for MessageFlow generation"
        )
    
    # Input Validation
    st.markdown("---")
    missing_inputs = []
    if not msgflow_template:
        missing_inputs.append("MessageFlow XML Template")
    if not confluence_doc:
        missing_inputs.append("Business Requirements Document")
    if not biztalk_maps_path or not os.path.exists(biztalk_maps_path):
        missing_inputs.append("Valid BizTalk Maps Path")
    if not groq_api_key:
        missing_inputs.append("GROQ API Key")
    
    if missing_inputs:
        st.error(f"🔒 **Missing Required Inputs**: {', '.join(missing_inputs)}")
        if not groq_api_key:
            st.code("export GROQ_API_KEY='your-api-key-here'", language='bash')
        return
    
    # Generation Section
    st.subheader("🚀 MessageFlow Generation")
    st.info("🎯 Generate enterprise-ready ACE MessageFlow with BizTalk transformation logic")
    
    if st.button("⚡ **Generate MessageFlow**", type="primary", key="generate_messageflow"):
        run_messageflow_generation(
            mapping_file=mapping_file,
            msgflow_template=msgflow_template,
            confluence_doc=confluence_doc,
            biztalk_maps_path=biztalk_maps_path,
            app_name=app_name,
            flow_name=flow_name,
            groq_api_key=groq_api_key,
            groq_model=groq_model
        )


def run_messageflow_generation(mapping_file, msgflow_template, confluence_doc, biztalk_maps_path, 
                             app_name, flow_name, groq_api_key, groq_model):
    """Execute MessageFlow generation with progress tracking"""
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    try:
        # Update progress tracking
        st.session_state.pipeline_progress['program_2']['status'] = 'running'
        progress_placeholder.progress(0)
        status_placeholder.info("🎯 Initializing MessageFlow Generator...")
        
        # Read uploaded files
        progress_placeholder.progress(20)
        status_placeholder.info("📄 Reading input files...")
        
        # Read MessageFlow template
        msgflow_content = msgflow_template.read().decode('utf-8')
        msgflow_template.seek(0)
        
        # Read Confluence document
        confluence_content = ""
        if confluence_doc.name.endswith('.pdf'):
            status_placeholder.warning("📄 PDF processing - extracting text...")
            # For PDF, you might need additional processing
            confluence_content = f"PDF Document: {confluence_doc.name} - Content processing required"
        elif confluence_doc.name.endswith(('.html', '.htm')):
            confluence_content = confluence_doc.read().decode('utf-8')
        elif confluence_doc.name.endswith('.txt'):
            confluence_content = confluence_doc.read().decode('utf-8')
        else:
            confluence_content = confluence_doc.read().decode('utf-8')
        
        confluence_doc.seek(0)
        
        # Import and run MessageFlow generator
        progress_placeholder.progress(40)
        status_placeholder.info("🤖 Starting MessageFlow generation with LLM...")
        
        from messageflow_generator import run_messageflow_generator
        
        result = run_messageflow_generator(
            mapping_file=mapping_file,
            msgflow_template_content=msgflow_content,
            confluence_content=confluence_content,
            biztalk_maps_path=biztalk_maps_path,
            app_name=app_name,
            flow_name=flow_name,
            groq_api_key=groq_api_key,
            groq_model=groq_model
        )
        
        progress_placeholder.progress(100)
        
        if result['success']:
            # Update session state
            st.session_state.pipeline_progress['program_2'] = {
                'status': 'success',
                'output': result['messageflow_file'],
                'timestamp': datetime.now().isoformat()
            }
            
            status_placeholder.success("✅ MessageFlow generation completed successfully!")
            
            # Display results
            st.success("🎉 **MessageFlow Generated Successfully!**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("📄 **Generated File**")
                st.code(os.path.basename(result['messageflow_file']))
                st.info("📊 **Processing Summary**")
                st.write(f"• BizTalk Maps Processed: {result.get('biztalk_maps_processed', 0)}")
                st.write(f"• Validation Status: {'✅ Passed' if result['validation']['valid'] else '❌ Failed'}")
            
            with col2:
                st.info("📁 **Output Location**")
                st.code(os.path.dirname(result['messageflow_file']))
                
                # Download button
                if os.path.exists(result['messageflow_file']):
                    with open(result['messageflow_file'], 'r') as f:
                        msgflow_xml = f.read()
                    
                    st.download_button(
                        label="📥 Download MessageFlow",
                        data=msgflow_xml,
                        file_name=f"{flow_name}.msgflow",
                        mime="application/xml",
                        key="download_messageflow"
                    )
            
            # Show validation details if any issues
            if not result['validation']['valid']:
                st.warning("⚠️ **Validation Issues Found**")
                for error in result['validation']['errors']:
                    st.error(f"• {error}")
        else:
            raise Exception("MessageFlow generation failed - check logs")
            
    except Exception as e:
        # Update session state
        st.session_state.pipeline_progress['program_2']['status'] = 'failed'
        progress_placeholder.progress(0)
        
        # Display error
        status_placeholder.error(f"❌ MessageFlow generation failed!")
        st.error(f"**Error Details**: {str(e)}")
        
        # Show error details in expander
        with st.expander("🔍 Full Error Details"):
            import traceback
            st.code(traceback.format_exc())
        
        # Helpful error messages
        error_msg = str(e).lower()
        if "api" in error_msg and "key" in error_msg:
            st.error("🔑 Please check your GROQ API key")
        elif "path" in error_msg or "file" in error_msg:
            st.error("📁 Please verify your BizTalk maps path and file uploads")
        elif "llm" in error_msg or "model" in error_msg:
            st.error("🤖 LLM processing failed - check your model selection and API limits")
        else:
            st.error("💡 Check input files and try again")


# Update the main pipeline progress initialization to include Program 2
def initialize_pipeline_progress():
    """Initialize pipeline progress tracking"""
    if 'pipeline_progress' not in st.session_state:
        st.session_state.pipeline_progress = {
            'program_1': {'status': 'pending', 'output': None},
            'program_2': {'status': 'pending', 'output': None},  # MessageFlow only
            'program_3': {'status': 'pending', 'output': None},
            'program_4': {'status': 'pending', 'output': None},
            'program_5': {'status': 'pending', 'output': None}
        }



def render_program_3_ui():
    """Render Program 3: ACE Module Creator UI - Updated for comprehensive BizTalk migration"""
    st.header("🏗️ Agent 3: ACE Module Creator")
    st.markdown("**Comprehensive BizTalk to ACE Migration** - Generate complete ESQL modules, XSL transformations, and enrichment files")
    
    # Check prerequisites
    prog2_status = st.session_state.pipeline_progress['program_2']['status']
    
    if prog2_status != 'success':
        st.warning("⚠️ Program 2 must be completed first to generate ACE foundation structure")
        return
    
    # Show Program 2 output info
    foundation_dir = st.session_state.pipeline_progress['program_2']['output']
    st.info(f"📁 **ACE Foundation Ready**: {os.path.basename(foundation_dir)}")
    
    # Required Inputs Section
    st.subheader("📋 Required Inputs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**1. BizTalk Project Root Directory**")
        biztalk_root_dir = st.text_input(
            "BizTalk Root Directory",
            value="C:\\@Official\\@Gen AI\\DSV\\BizTalk\\MH.ESB.EE.Out.DocPackApp\\MH.ESB.EE.Out.DocPackApp\\MH.ESB.EE.Out.DocPackApp",
            help="Complete path to BizTalk project root containing all .btproj, .odx, .btm, .xsl files",
            key="prog3_biztalk_root"
        )
        
        # Validate BizTalk directory
        if biztalk_root_dir and os.path.exists(biztalk_root_dir):
            # Quick scan to show what will be discovered
            biztalk_files = []
            for root, dirs, files in os.walk(biztalk_root_dir):
                if len(biztalk_files) >= 10:  # Limit for UI display
                    break
                for file in files[:5]:  # Limit per directory
                    if any(file.lower().endswith(ext) for ext in ['.btproj', '.odx', '.btm', '.xsl', '.cs']):
                        biztalk_files.append(file)
            
            if biztalk_files:
                st.success(f"✅ Found {len(biztalk_files)}+ BizTalk files")
                with st.expander(f"📁 Preview: {len(biztalk_files)} files discovered"):
                    for file in biztalk_files:
                        file_icon = "📁" if file.endswith('.btproj') else \
                                   "🔄" if file.endswith(('.odx', '.btm')) else \
                                   "🔧" if file.endswith('.cs') else \
                                   "🗺️" if file.endswith(('.xsl', '.xslt')) else "📄"
                        st.text(f"{file_icon} {file}")
            else:
                st.warning("⚠️ No BizTalk files found - check directory path")
        elif biztalk_root_dir:
            st.error("❌ Directory does not exist")
    
    with col2:
        st.markdown("**2. Business Context Document (Optional)**")
        confluence_pdf = st.file_uploader(
            "Upload Confluence/Business Requirements PDF",
            type=['pdf'],
            help="Business requirements document for domain-specific ESQL generation",
            key="prog3_confluence_pdf"
        )
        
        if confluence_pdf:
            st.success(f"✅ Document uploaded: {confluence_pdf.name}")
            st.info(f"📊 Size: {confluence_pdf.size / 1024:.1f} KB")

    # AI Configuration Section  
    with st.expander("🤖 AI Configuration", expanded=True):
        col3, col4 = st.columns(2)
        
        with col3:
            groq_api_key = st.text_input(
                "GROQ API Key", 
                value=os.getenv('GROQ_API_KEY', ''), 
                type="password",
                key="prog3_groq_key",
                help="Get your API key from https://console.groq.com/"
            )
            
            groq_model = st.selectbox(
                "GROQ Model",
                ["llama3-70b-8192", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
                help="Choose the AI model for ESQL and XSL generation"
            )
        
        with col4:
            generation_scope = st.multiselect(
                "Generation Scope",
                [
                    "Core ESQL Modules",
                    "Database Enrichment", 
                    "XSL Transformations",
                    "Business Logic",
                    "Error Handling",
                    "Validation Procedures"
                ],
                default=[
                    "Core ESQL Modules", 
                    "Database Enrichment", 
                    "XSL Transformations",
                    "Business Logic"
                ],
                help="Select which components to generate with AI"
            )
            
            temperature = st.slider(
                "AI Creativity", 
                min_value=0.0, 
                max_value=1.0, 
                value=0.1,
                help="0.0 = Conservative/Precise, 1.0 = Creative/Experimental"
            )

    # Input validation
    input_validation = True
    validation_messages = []
    
    if not groq_api_key:
        validation_messages.append("🔑 GROQ API Key required")
        input_validation = False
        
    if not biztalk_root_dir or not os.path.exists(biztalk_root_dir):
        validation_messages.append("📁 Valid BizTalk root directory required")  
        input_validation = False
    
    # Show validation messages
    if validation_messages:
        for msg in validation_messages:
            st.error(msg)
    
    # Generation Preview
    if input_validation:
        st.subheader("📊 Generation Preview")
        
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            st.metric("ESQL Modules", "8-15", help="Core processing, validation, error handling")
        with col6:
            st.metric("XSL Files", "2-8", help="Data transformations, map conversions")  
        with col7:
            st.metric("Enrichment", "3-7", help="Database lookup procedures")
        with col8:
            st.metric("Total Files", "15-35", help="Complete ACE project structure")

    # Execution Button
    if input_validation:
        if st.button("🏗️ Generate ACE Modules", type="primary", key="run_prog3", help="Start comprehensive BizTalk to ACE migration"):
            run_program_3(groq_api_key, groq_model, biztalk_root_dir, confluence_pdf, generation_scope, temperature)
    else:
        st.button("🏗️ Generate ACE Modules", disabled=True, help="Fix validation errors first")


def run_program_3(groq_api_key, groq_model, biztalk_root_dir, confluence_pdf, generation_scope, temperature):
    """Execute Program 3 - ACE Module Creator"""
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    try:
        st.session_state.pipeline_progress['program_3']['status'] = 'running'
        progress_placeholder.progress(0)
        status_placeholder.info("🏗️ Initializing ACE Module Creator...")
        
        # Set environment variable
        os.environ['GROQ_API_KEY'] = groq_api_key
        
        # Get Program 2 output and ensure it's a directory
        foundation_dir = st.session_state.pipeline_progress['program_2']['output']
        
        # Handle case where Program 2 returns a file path instead of directory
        if foundation_dir and os.path.isfile(foundation_dir):
            foundation_dir = os.path.dirname(foundation_dir)
        
        # Validate foundation directory
        if not foundation_dir or not os.path.exists(foundation_dir):
            st.error("❌ Invalid foundation directory from Program 2")
            return
            
        progress_placeholder.progress(10)
        status_placeholder.info(f"📁 Foundation directory: {os.path.basename(foundation_dir)}")
        
        # Initialize ACE Module Creator
        from ace_module_creator import ACEModuleCreator
        creator = ACEModuleCreator()
        creator.config["groq_settings"]["model"] = groq_model
        creator.config["groq_settings"]["temperature"] = temperature
        
        progress_placeholder.progress(20)
        status_placeholder.info("🔍 Scanning BizTalk root directory...")
        
        # Load foundation structure
        creator.load_foundation_structure(foundation_dir)
        
        progress_placeholder.progress(30)
        status_placeholder.info("🔬 Analyzing BizTalk components...")
        
        # Prepare confluence PDF path if uploaded
        confluence_pdf_path = None
        if confluence_pdf:
            # Save uploaded PDF to temporary location
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(confluence_pdf.getvalue())
                confluence_pdf_path = tmp_file.name
        
        # Debug information and validation
        st.info(f"🔍 **Debug Information:**")
        st.text(f"Foundation Dir: {foundation_dir}")
        st.text(f"BizTalk Root: {biztalk_root_dir}")
        st.text(f"Confluence PDF: {confluence_pdf_path or 'None'}")
        
        # Check for messageflow files in foundation directory
        msgflow_files = []
        if os.path.isdir(foundation_dir):
            msgflow_files = list(Path(foundation_dir).glob('*.msgflow'))
            
        if msgflow_files:
            st.success(f"✅ Found {len(msgflow_files)} messageflow file(s)")
            for msgflow in msgflow_files:
                st.text(f"  📊 {msgflow.name}")
        else:
            st.warning("⚠️ No messageflow files found in foundation directory")
            st.text("Expected location: Foundation directory should contain .msgflow files")
        
        progress_placeholder.progress(50)
        status_placeholder.info("⚡ Generating ESQL modules and XSL transformations...")
        
        # Run ACE Module Creator
        enhanced_dir = creator.enhance(
            foundation_dir=foundation_dir,
            biztalk_root_dir=biztalk_root_dir,
            confluence_pdf=confluence_pdf_path,
            output_dir=None  # Let it auto-generate
        )
        
        progress_placeholder.progress(80)
        status_placeholder.info("📋 Generating migration documentation...")
        
        progress_placeholder.progress(100)
        
        # Update session state
        st.session_state.pipeline_progress['program_3']['status'] = 'success'
        st.session_state.pipeline_progress['program_3']['output'] = enhanced_dir
        
        # Success message with detailed statistics
        esql_count = len([f for f in creator.generated_files if f.endswith('.esql')])
        xsl_count = len([f for f in creator.generated_files if f.endswith('.xsl')])
        total_components = creator.biztalk_analysis['discovery_summary']['total_components'] if creator.biztalk_analysis else 0
        
        status_placeholder.success(
            f"✅ ACE Module Creator completed successfully! "
            f"Generated {len(creator.generated_files)} files from {total_components} BizTalk components"
        )
        
        # Detailed Results Section
        st.subheader("🎉 Generation Results")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📄 Total Files", len(creator.generated_files))
        with col2:
            st.metric("⚡ ESQL Modules", esql_count)
        with col3:
            st.metric("🔄 XSL Transforms", xsl_count)
        with col4:
            st.metric("🔍 BizTalk Components", total_components)
        
        # Generated Files Display
        with st.expander("📁 Generated Files Details", expanded=True):
            # Group files by type
            file_groups = {
                'ESQL Modules': [f for f in creator.generated_files if f.endswith('.esql')],
                'XSL Transformations': [f for f in creator.generated_files if f.endswith('.xsl')],
                'Project Files': [f for f in creator.generated_files if f.endswith(('.project', '.json'))],
                'Documentation': [f for f in creator.generated_files if f.endswith('.md')]
            }
            
            for group_name, files in file_groups.items():
                if files:
                    st.markdown(f"**{group_name}** ({len(files)} files)")
                    for file_path in files:
                        file_name = os.path.basename(file_path)
                        relative_path = os.path.relpath(file_path, enhanced_dir)
                        
                        # Determine icon
                        if 'enrichment' in file_path.lower():
                            icon = "🔍"
                            file_type = "Enrichment"
                        elif file_path.endswith('.esql'):
                            icon = "⚡"
                            file_type = "ESQL"
                        elif file_path.endswith('.xsl'):
                            icon = "🔄"
                            file_type = "XSL"
                        elif file_path.endswith('.project'):
                            icon = "📁"
                            file_type = "Project"
                        else:
                            icon = "📄"
                            file_type = "Other"
                        
                        st.text(f"  {icon} {file_name} ({file_type})")
        
        # Migration Summary
        with st.expander("📊 Migration Summary"):
            if creator.biztalk_analysis:
                analysis = creator.biztalk_analysis
                
                st.markdown("**BizTalk Analysis:**")
                st.text(f"📁 Project: {analysis['project_structure']['name']}")
                st.text(f"🔄 Business Processes: {len(analysis['business_processes'])}")
                st.text(f"🗺️ Data Transformations: {len(analysis['data_transformations'])}")
                st.text(f"🔧 XSL Transformations: {len(analysis.get('xsl_transformations', []))}")
                st.text(f"💻 Custom Components: {len(analysis['custom_components'])}")
                st.text(f"🔍 Enrichment Requirements: {len(analysis.get('enrichment_requirements', []))}")
                
                st.markdown("**Generation Context:**")
                st.text(f"📋 Business Context Used: {'Yes' if creator.confluence_used else 'No'}")
                st.text(f"🤖 AI Model Used: {groq_model}")
                st.text(f"🎯 Generation Scope: {', '.join(generation_scope)}")
        
        # Next Steps
        st.subheader("🚀 Next Steps")
        st.markdown("""
        **Your ACE project is ready! Here's what to do next:**
        
        1. **📁 Import into ACE Toolkit**: Import the generated `.project` file
        2. **🔍 Review Generated Code**: Examine ESQL modules and XSL transformations  
        3. **⚙️ Configure Databases**: Set up database connections for enrichment modules
        4. **🧪 Test Message Flows**: Create test cases and validate business logic
        5. **📋 Check Migration Report**: Review the detailed migration analysis in `/docs/`
        
        **Generated Files Location:**
        """)
        st.code(enhanced_dir, language='text')
        
        # Clean up temporary PDF file if created
        if confluence_pdf_path and os.path.exists(confluence_pdf_path):
            try:
                os.unlink(confluence_pdf_path)
            except:
                pass  # Ignore cleanup errors
        
    except Exception as e:
        st.session_state.pipeline_progress['program_3']['status'] = 'error'
        status_placeholder.error(f"❌ ACE Module Creator failed: {str(e)}")
        
        # Show detailed error information
        with st.expander("🔍 Error Details"):
            import traceback
            st.code(traceback.format_exc(), language='python')
        
        # Cleanup on error
        if 'confluence_pdf_path' in locals() and confluence_pdf_path and os.path.exists(confluence_pdf_path):
            try:
                os.unlink(confluence_pdf_path)
            except:
                pass

def create_zip_buffer(directory_path):
    """Create a ZIP file buffer from a directory for download"""
    import zipfile
    import io
    
    zip_buffer = io.BytesIO()
    
    try:
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Create archive path relative to the base directory
                    archive_name = os.path.relpath(file_path, directory_path)
                    zipf.write(file_path, archive_name)
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
        
    except Exception as e:
        print(f"❌ Failed to create ZIP: {e}")
        return None

def render_program_4_ui():
    """Render Program 4: Migration Quality Reviewer UI"""
    st.header("🔍 Agent 4: Migration Quality Reviewer")
    st.markdown("Validate enhanced components and generate deployment artifacts")
    
    # Check prerequisites
    prog3_status = st.session_state.pipeline_progress['program_3']['status']
    
    if prog3_status != 'success':
        st.warning("⚠️ Program 3 must be completed first")
        return
    
    # Configuration
    with st.expander("🔍 Quality Review Configuration"):
        col1, col2 = st.columns(2)
        
        with col1:
            quality_thresholds = st.slider(
                "Quality Threshold (%)",
                min_value=70,
                max_value=100,
                value=85,
                help="Minimum quality score for deployment approval"
            )
            
            include_groq_validation = st.checkbox(
                "AI-Powered Validation",
                value=True,
                help="Use GROQ for functional equivalence analysis"
            )
        
        with col2:
            validation_scope = st.multiselect(
                "Validation Scope",
                ["Syntax Check", "Functional Equivalence", "Code Quality", "Security Scan"],
                default=["Syntax Check", "Functional Equivalence", "Code Quality"],
                help="Select validation areas"
            )
            
            generate_bar_file = st.checkbox(
                "Generate BAR File",
                value=True,
                help="Create deployment-ready BAR file"
            )
    
    # Account-Specific Customization
    with st.expander("🎯 Account Customization (Optional)", expanded=False):
        st.markdown("Upload your company-specific details to customize generated ACE modules with your actual values. \n " \
        "This helps to align the modules with DSV standards and practices.")
        
        # File uploader for account-specific input
        uploaded_account_file = st.file_uploader(
            "Upload Requirements File",
            type=['json', 'xml', 'txt'],
            help="Company codes, database settings, queue names, etc. which shall help to enhance the ACE moduls to match DSV standards."
        )
        
        if uploaded_account_file:
            st.success("✅ File uploaded - ACE modules will be customized with your values")
        
    
    # ACE Library Configuration
    with st.expander("📚 ACE Library Validation", expanded=False):
        library_path = st.text_input(
            "ACE Libraries Path",
            value=r"C:\@Official\@Gen AI\DSV\BizTalk\Analyze_this_folder\libraries",
            help="Path to your ACE libraries for validation against mapping requirements"
        )
        
        validate_libraries = st.checkbox(
            "Validate Required Libraries",
            value=True,
            help="Check if all mapped ACE libraries exist and scan their contents"
        )
        
        if validate_libraries:
            st.info("📋 The system will scan for .esql, .subflow files in your library path and validate against Agent 2 mapping")
    
    # Original BizTalk path for comparison
    original_biztalk_path = st.text_input(
        "Original BizTalk Path (for comparison)",
        value=r"C:\@Official\@Gen AI\DSV\BizTalk\MH.ESB.EE.Out.DocPackApp\MH.ESB.EE.Out.DocPackApp",
        help="Path to original BizTalk components for comparison"
    )
    
    # Output configuration
    with st.expander("📁 Output Configuration"):
        output_folder_name = st.text_input(
            "Output Folder Name",
            value="Agent_4_Reviewed_Modules",
            help="Name for the final reviewed modules folder"
        )
        
        include_enrichment_files = st.checkbox(
            "Generate Enrichment Files",
            value=True,
            help="Create before_enrichment.json and after_enrichment.json files"
        )
    
    # Execution
    if st.button("🔍 Run Agent 4", type="primary", key="run_prog4"):
        # Prepare account input
        account_input_data = None
        if uploaded_account_file:
            account_input_data = uploaded_account_file.read().decode('utf-8')
        
        run_program_4(
            quality_thresholds=quality_thresholds,
            include_groq_validation=include_groq_validation, 
            validation_scope=validation_scope,
            generate_bar_file=generate_bar_file,
            original_biztalk_path=original_biztalk_path,
            account_input_data=account_input_data,
            library_path=library_path,
            validate_libraries=validate_libraries,
            output_folder_name=output_folder_name,
            include_enrichment_files=include_enrichment_files
        )

def run_program_4(quality_thresholds, include_groq_validation, validation_scope, 
                 generate_bar_file, original_biztalk_path, account_input_data=None,
                 library_path=None, validate_libraries=True,
                 output_folder_name="reviewed_modules", include_enrichment_files=True):
    """Execute Program 4 with enhanced account-specific features"""
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    try:
        st.session_state.pipeline_progress['program_4']['status'] = 'running'
        progress_placeholder.progress(0)
        status_placeholder.info("📄 Initializing Enhanced Quality Reviewer...")
        
        # Get inputs from previous programs
        enhanced_dir = st.session_state.pipeline_progress['program_3']['output']
        mapping_file = st.session_state.pipeline_progress['program_1']['output']
        
        # FIX: Calculate the GENAI_ACE root folder path for comprehensive scanning
        # enhanced_dir typically points to: .../GENAI_ACE/.../ace_modules_enhanced
        # We need to scan from GENAI_ACE root to find all .msgflow, .project, .esql, .xsl files
        enhanced_path = Path(enhanced_dir)
        
        # Navigate up the directory tree to find GENAI_ACE folder
        genai_ace_root = None
        current_path = enhanced_path
        max_levels = 10  # Safety limit to prevent infinite loop
        level_count = 0
        
        while current_path.parent != current_path and level_count < max_levels:
            if current_path.name == "GENAI_ACE":
                genai_ace_root = current_path
                break
            current_path = current_path.parent
            level_count += 1
        
        # If GENAI_ACE not found, fall back to going up 3 levels from enhanced_dir
        if not genai_ace_root:
            genai_ace_root = enhanced_path.parent.parent.parent
            st.warning(f"⚠️ GENAI_ACE folder not found by name, using calculated path: {genai_ace_root}")
        
        # Validate the calculated root path exists
        if not genai_ace_root.exists():
            st.error(f"❌ Calculated GENAI_ACE root path does not exist: {genai_ace_root}")
            return
        
        st.info(f"🔍 Scanning ACE root: {genai_ace_root}")
        st.info(f"📁 This will find .msgflow, .project, .esql, .xsl files in ALL subfolders")
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(mapping_file), "final_quality_report")
        os.makedirs(output_dir, exist_ok=True)
        
        # Save account input to temporary file if provided
        account_input_path = None
        if account_input_data:
            account_input_path = os.path.join(output_dir, "account_input.txt")
            with open(account_input_path, 'w', encoding='utf-8') as f:
                f.write(account_input_data)
            status_placeholder.info("🎯 Account-specific input loaded - components will be customized!")
        
        progress_placeholder.progress(15)
        status_placeholder.info("📄 Setting up Enhanced Migration Quality Reviewer...")
        
        # Validate required inputs
        if not library_path or not os.path.exists(library_path):
            st.error(f"❌ Library path not found: {library_path}")
            return
        
        # Initialize enhanced reviewer with CORRECTED ROOT PATH
        from migration_quality_reviewer import MigrationQualityReviewer
        confluence_path = st.session_state.get('program_3_confluence_path', None)

        reviewer = MigrationQualityReviewer(
            ace_migrated_folder=str(genai_ace_root),  # FIXED: Use GENAI_ACE root instead of enhanced_dir subfolder
            mapping_excel_path=mapping_file,
            library_path=library_path,
            account_input_path=account_input_path,
            confluence_path=confluence_path,
            output_folder_name=output_folder_name
        )
        
        progress_placeholder.progress(30)
        status_placeholder.info("📚 Validating ACE libraries and dependencies...")
        
        # Run enhanced quality review
        final_output_path = reviewer.run_quality_review() 
        
        progress_placeholder.progress(100)
        
        # Update session state
        st.session_state.pipeline_progress['program_4']['status'] = 'success'
        st.session_state.pipeline_progress['program_4']['output'] = final_output_path
        
        # Display results
        library_validation = reviewer.review_data.get('library_validation', {})
        validation_summary = library_validation.get('validation_summary', {})
        
        status_placeholder.success("✅ Enhanced Quality Review completed!")
        
        # Show enhanced results summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            success_rate = validation_summary.get('success_rate', 0)
            st.metric(
                "Library Validation", 
                f"{success_rate:.1f}%",
                delta="Excellent" if success_rate >= 90 else "Good" if success_rate >= 75 else "Needs Attention"
            )
        
        with col2:
            customizations_applied = "Yes" if account_input_data else "No"
            st.metric("Account Customizations", customizations_applied)
        
        with col3:
            found_libs = validation_summary.get('found', 0)
            total_libs = validation_summary.get('total_required', 0)
            st.metric("Libraries Found", f"{found_libs}/{total_libs}")
        
        # Enhanced download buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download final modules as ZIP
            if os.path.exists(final_output_path):
                zip_buffer = create_zip_buffer(final_output_path)
                st.download_button(
                    label="📦 Download Enhanced Modules",
                    data=zip_buffer,
                    file_name=f"enhanced_ace_modules_{reviewer.timestamp}.zip",
                    mime="application/zip",
                    help="Complete enhanced ACE modules ready for deployment"
                )
        
        with col2:
            # Download detailed review report
            review_report_path = os.path.join(os.path.dirname(final_output_path), f"llm_quality_review_{reviewer.timestamp}.json")
            if os.path.exists(review_report_path):
                with open(review_report_path, 'r') as f:
                    report_data = f.read()
                st.download_button(
                    label="📊 Download Review Report", 
                    data=report_data,
                    file_name=f"quality_review_report_{reviewer.timestamp}.json",
                    mime="application/json",
                    help="Detailed LLM analysis and enhancement report"
                )
        
        with col3:
            # Download library validation report
            if library_validation:
                library_report = json.dumps(library_validation, indent=2)
                st.download_button(
                    label="📚 Download Library Report",
                    data=library_report,
                    file_name=f"library_validation_{reviewer.timestamp}.json", 
                    mime="application/json",
                    help="ACE library validation and dependency analysis"
                )
    
    except Exception as e:
        st.session_state.pipeline_progress['program_4']['status'] = 'error' 
        st.session_state.pipeline_progress['program_4']['error'] = str(e)
        status_placeholder.error(f"❌ Enhanced Quality Review failed: {e}")
        st.error(f"Error details: {e}")
        
        # Debug information
        st.expander("🔍 Debug Information").write({
            'enhanced_dir': enhanced_dir if 'enhanced_dir' in locals() else 'Not set',
            'genai_ace_root': str(genai_ace_root) if 'genai_ace_root' in locals() else 'Not calculated',
            'mapping_file': mapping_file if 'mapping_file' in locals() else 'Not set',
            'library_path': library_path,
        })


# UPDATED PROGRAM 5 UI - Postman Collection Generator Integration
def render_program_5_ui():
    """Render Program 5: Postman Collection Generator UI"""
    st.header("📦 Agent 5: Generate Postman Collections")
    st.markdown("Create comprehensive **Postman test collections** from IBM ACE Message Flows with 100+ test scenarios")
    
    # Check dependencies
    dependencies_check = check_postman_dependencies()
    if dependencies_check['all_available']:
        format_info = "✅ **Output**: Postman Collections + Environments + Test Data + Documentation"
    else:
        format_info = "⚠️ **Missing Dependencies**: " + ", ".join(dependencies_check['missing'])
    
    st.info(format_info)
    
    # Check if Program 4 completed
    program_4_status = st.session_state.pipeline_progress.get('program_4', {}).get('status')
    program_4_output = st.session_state.pipeline_progress.get('program_4', {}).get('output')
    
    if program_4_status != 'success' or not program_4_output:
        st.warning("⚠️ **Program 4 Required**: Complete Migration Quality Reviewer first to generate reviewed ACE components")
        st.info("📋 Program 5 needs the reviewed modules from Program 4 as input")
        return
    
    st.success(f"✅ **Input Ready**: {program_4_output}")
    
    # Configuration
    with st.expander("🔧 Configuration", expanded=True):
        # Project name
        project_name = st.text_input(
            "🎯 Project Name",
            value="ACE_MessageFlow_TestSuite",
            help="Name for the Postman collections and test scenarios"
        )
        
        # Output location (editable)
        default_output_path = get_default_postman_output_path(program_4_output)
        target_output_folder = st.text_input(
            "📁 Output Folder",
            value=default_output_path,
            help="Where to create the Postman collections folder"
        )
        
        # Validate output path
        if target_output_folder:
            output_parent = Path(target_output_folder).parent
            if output_parent.exists():
                st.success("✅ Valid output location")
            else:
                st.warning(f"⚠️ Parent directory doesn't exist: {output_parent}")
        
        col1, col2 = st.columns(2)
        with col1:
            # Confluence documentation (optional)
            use_confluence = st.checkbox("📄 Include Confluence Specification", value=False)
            
            # Advanced options
            generate_advanced_scenarios = st.checkbox("🧪 Advanced Test Scenarios", value=True, 
                                                     help="Include performance, security, and integration tests")
        
        with col2:
            # Environment configurations
            environment_count = st.selectbox("🌍 Environment Configurations", 
                                           options=[2, 3, 4], 
                                           index=1,  # Default to 3 environments
                                           help="Number of environment configs to generate")
            
            # LLM enhancement (optional)
            use_llm_enhancement = st.checkbox("🤖 AI-Enhanced Payloads", value=True,
                                            help="Use AI to generate more realistic test payloads")
        
        # Confluence file input
        confluence_pdf_path = None
        if use_confluence:
            confluence_file = st.file_uploader(
                "📄 Upload Confluence Specification",
                type=['pdf', 'txt', 'md'],
                help="Technical specification document for enhanced test scenarios"
            )
            if confluence_file:
                # Save uploaded file temporarily
                confluence_pdf_path = save_uploaded_file(confluence_file, "confluence_spec")
        
        # LLM configuration
        if use_llm_enhancement:
            groq_api_key = st.text_input(
                "🔑 GROQ API Key", 
                value=os.getenv('GROQ_API_KEY', ''), 
                type="password",
                help="For AI-enhanced payload generation"
            )
            if groq_api_key:
                os.environ['GROQ_API_KEY'] = groq_api_key
    
    # Quick analysis of input
    if st.button("🔍 Analyze Input Files", key="analyze_input"):
        analyze_ace_input_files(program_4_output)
    
    # Generation controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📦 Generate Collections", type="primary", key="run_postman_gen"):
            run_postman_collection_generation(
                reviewed_modules_path=program_4_output,
                confluence_pdf_path=confluence_pdf_path,
                target_output_folder=target_output_folder,
                project_name=project_name,
                generate_advanced_scenarios=generate_advanced_scenarios,
                environment_count=environment_count,
                use_llm_enhancement=use_llm_enhancement
            )
    
    with col2:
        if st.button("📊 Preview Test Scenarios", key="preview_scenarios"):
            preview_test_scenarios(program_4_output, project_name)
    
    with col3:
        if st.session_state.pipeline_progress.get('program_5', {}).get('status') == 'success':
            output_path = st.session_state.pipeline_progress['program_5']['output']
            if st.button("📁 Open Output Folder", key="open_output"):
                open_output_folder(output_path)

def check_postman_dependencies():
    """Check if required dependencies are available"""
    dependencies = {
        'xml.etree.ElementTree': True,  # Built-in
        'json': True,  # Built-in
        'pathlib': True,  # Built-in
    }
    
    optional_deps = {}
    try:
        from groq import Groq
        optional_deps['groq'] = True
    except ImportError:
        optional_deps['groq'] = False
    
    missing = [dep for dep, available in {**dependencies, **optional_deps}.items() if not available]
    
    return {
        'all_available': len(missing) == 0,
        'missing': missing,
        'optional_missing': [dep for dep, available in optional_deps.items() if not available]
    }

def get_default_postman_output_path(program_4_output):
    """Calculate default output path for Postman collections"""
    reviewed_modules_path = Path(program_4_output)
    root_folder = reviewed_modules_path.parent
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return str(root_folder / f"POSTMAN_TEST_COLLECTIONS_{timestamp}")

def save_uploaded_file(uploaded_file, prefix):
    """Save uploaded file temporarily"""
    import tempfile
    temp_dir = Path(tempfile.gettempdir())
    file_extension = Path(uploaded_file.name).suffix
    temp_file_path = temp_dir / f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
    
    with open(temp_file_path, 'wb') as f:
        f.write(uploaded_file.read())
    
    return str(temp_file_path)

def analyze_ace_input_files(program_4_output):
    """Analyze the ACE input files for preview"""
    if not Path(program_4_output).exists():
        st.error(f"❌ Input path not found: {program_4_output}")
        return
    
    try:
        from postman_collection_generator import PostmanCollectionGenerator
        
        # Create a temporary generator just for analysis
        temp_generator = PostmanCollectionGenerator(
            reviewed_modules_path=program_4_output,
            project_name="Analysis"
        )
        
        # Parse artifacts
        temp_generator._parse_ace_artifacts()
        
        st.success("🔍 **Input Analysis Results:**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Message Flows", len(temp_generator.ace_artifacts['msgflow_files']))
        with col2:
            st.metric("ESQL Modules", len(temp_generator.ace_artifacts['esql_modules']))
        with col3:
            st.metric("XSL Transforms", len(temp_generator.ace_artifacts['xsl_transforms']))
        with col4:
            st.metric("Project Files", len(temp_generator.ace_artifacts['project_configs']))
        
        # Show discovered endpoints
        endpoints_found = []
        for msgflow in temp_generator.ace_artifacts['msgflow_files']:
            if 'error' not in msgflow:
                endpoints = msgflow.get('endpoints', {})
                endpoints_found.extend(endpoints.get('http_inputs', []))
                endpoints_found.extend(endpoints.get('mq_inputs', []))
        
        if endpoints_found:
            st.info(f"🎯 **Discovered {len(endpoints_found)} endpoints** for test generation")
            with st.expander("📋 Endpoint Details"):
                for i, endpoint in enumerate(endpoints_found[:5]):  # Show first 5
                    if 'url_suffix' in endpoint:  # HTTP endpoint
                        st.write(f"{i+1}. **HTTP**: {endpoint.get('http_method', 'POST')} {endpoint['url_suffix']}")
                    elif 'queue_name' in endpoint:  # MQ endpoint
                        st.write(f"{i+1}. **MQ**: {endpoint['queue_name']}")
        else:
            st.warning("⚠️ No endpoints discovered. Check input files.")
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {e}")

def preview_test_scenarios(program_4_output, project_name):
    """Preview what test scenarios will be generated"""
    try:
        from postman_collection_generator import PostmanCollectionGenerator
        
        temp_generator = PostmanCollectionGenerator(
            reviewed_modules_path=program_4_output,
            project_name=project_name
        )
        
        # Get test templates
        test_templates = temp_generator.test_templates
        
        st.info("🧪 **Test Scenarios Preview:**")
        
        total_scenarios = 0
        for category_name, category_data in test_templates.items():
            with st.expander(f"📋 {category_name.replace('_', ' ').title()}"):
                category_total = 0
                for test_type, test_config in category_data.items():
                    st.write(f"**{test_config['name']}** (Priority {test_config['priority']})")
                    st.write(f"*{test_config['description']}*")
                    
                    for scenario in test_config['scenarios']:
                        st.write(f"  • {scenario}")
                        category_total += 1
                    
                    st.write("---")
                
                st.write(f"**Category Total: {category_total} scenarios**")
                total_scenarios += category_total
        
        st.success(f"🎯 **Estimated Total: {total_scenarios}+ test scenarios**")
        st.info("*Actual count will be higher with entity-specific and endpoint-specific tests*")
        
    except Exception as e:
        st.error(f"❌ Preview failed: {e}")

def run_postman_collection_generation(reviewed_modules_path, confluence_pdf_path, target_output_folder, 
                                    project_name, generate_advanced_scenarios, environment_count, use_llm_enhancement):
    """Execute Postman collection generation"""
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    try:
        st.session_state.pipeline_progress['program_5']['status'] = 'running'
        progress_placeholder.progress(0)
        status_placeholder.info("📦 Initializing Postman Collection Generator...")
        
        # Import the generator
        from postman_collection_generator import PostmanCollectionGenerator
        
        # Create generator instance
        generator = PostmanCollectionGenerator(
            reviewed_modules_path=reviewed_modules_path,
            confluence_pdf_path=confluence_pdf_path,
            target_output_folder=target_output_folder,
            project_name=project_name
        )
        
        progress_placeholder.progress(20)
        status_placeholder.info("🔍 Analyzing IBM ACE artifacts...")
        
        # Generate collections
        output_path = generator.generate_postman_collections()
        
        progress_placeholder.progress(100)
        
        # Update session state
        st.session_state.pipeline_progress['program_5']['status'] = 'success'
        st.session_state.pipeline_progress['program_5']['output'] = output_path
        
        status_placeholder.success("✅ Postman Collections Generated Successfully!")
        
        # Display results
        results = generator.generation_results
        
        st.balloons()
        
        # Results metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 Collections Created", len(results['collections_created']))
        with col2:
            st.metric("🧪 Test Scenarios", results['test_scenarios_generated'])
        with col3:
            st.metric("🌍 Environments", len(results['environments_created']))
        with col4:
            st.metric("📊 Test Data Samples", results['payload_samples_created'])
        
        # Generated files summary
        with st.expander("📁 Generated Files", expanded=True):
            st.write("**📦 Postman Collections:**")
            for collection_file in results['collections_created']:
                collection_name = Path(collection_file).name
                st.write(f"  • {collection_name}")
            
            st.write("**🌍 Environment Configurations:**")
            for env_file in results['environments_created']:
                env_name = Path(env_file).name
                st.write(f"  • {env_name}")
            
            st.write("**📚 Documentation Files:**")
            for doc_file in results['documentation_files']:
                doc_name = Path(doc_file).name
                st.write(f"  • {doc_name}")
        
        # Download options
        st.write("### 📥 Download Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📦 Download Main Collection", key="download_main"):
                download_main_collection(results['collections_created'])
        
        with col2:
            if st.button("🌍 Download Environments", key="download_envs"):
                download_environments(results['environments_created'])
        
        with col3:
            if st.button("📚 Download Documentation", key="download_docs"):
                download_documentation(results['documentation_files'])
        
        # Quick setup guide
        with st.expander("🚀 Quick Setup Guide", expanded=True):
            st.markdown(f"""
            **Next Steps:**
            1. **Import Collections**: Import all `.postman_collection.json` files into Postman
            2. **Configure Environments**: Update environment variables with your server details
            3. **Set Authentication**: Add valid tokens to each environment
            4. **Run Tests**: Start with functional tests, then expand to full suite
            
            **Output Location**: `{output_path}`
            
            **Automation Ready**: Use Newman CLI for CI/CD integration
            ```bash
            newman run "{project_name}_Complete_TestSuite.postman_collection.json" \\
              -e "Development.postman_environment.json" \\
              --reporters cli,html
            ```
            """)
        
    except Exception as e:
        st.session_state.pipeline_progress['program_5']['status'] = 'error'
        status_placeholder.error(f"❌ Generation failed: {str(e)}")
        
        # Show detailed error for debugging
        import traceback
        error_details = traceback.format_exc()
        with st.expander("🔧 Error Details"):
            st.code(error_details)

def download_main_collection(collections_created):
    """Download the main Postman collection"""
    try:
        main_collection = None
        for collection_path in collections_created:
            if "Complete_TestSuite" in collection_path:
                main_collection = collection_path
                break
        
        if not main_collection:
            main_collection = collections_created[0]  # Fallback to first collection
        
        with open(main_collection, 'rb') as f:
            collection_data = f.read()
        
        st.download_button(
            label="📦 Download Main Collection",
            data=collection_data,
            file_name=Path(main_collection).name,
            mime="application/json",
            key="download_main_collection"
        )
        
    except Exception as e:
        st.error(f"Download failed: {e}")

def download_environments(environments_created):
    """Download environment configurations as a zip file"""
    try:
        import zipfile
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            with zipfile.ZipFile(tmp_file.name, 'w') as zipf:
                for env_file in environments_created:
                    zipf.write(env_file, Path(env_file).name)
            
            with open(tmp_file.name, 'rb') as f:
                zip_data = f.read()
            
            st.download_button(
                label="🌍 Download All Environments",
                data=zip_data,
                file_name="postman_environments.zip",
                mime="application/zip",
                key="download_environments_zip"
            )
    
    except Exception as e:
        st.error(f"Environment download failed: {e}")

def download_documentation(documentation_files):
    """Download documentation files as a zip"""
    try:
        import zipfile
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            with zipfile.ZipFile(tmp_file.name, 'w') as zipf:
                for doc_file in documentation_files:
                    zipf.write(doc_file, Path(doc_file).name)
            
            with open(tmp_file.name, 'rb') as f:
                zip_data = f.read()
            
            st.download_button(
                label="📚 Download Documentation",
                data=zip_data,
                file_name="postman_documentation.zip",
                mime="application/zip",
                key="download_docs_zip"
            )
    
    except Exception as e:
        st.error(f"Documentation download failed: {e}")

def open_output_folder(output_path):
    """Open the output folder in file explorer"""
    try:
        import subprocess
        import platform
        
        if platform.system() == "Windows":
            subprocess.run(['explorer', str(output_path)])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(['open', str(output_path)])
        else:  # Linux
            subprocess.run(['xdg-open', str(output_path)])
        
        st.success(f"📁 Opened: {output_path}")
        
    except Exception as e:
        st.error(f"Failed to open folder: {e}")
        st.info(f"Manual path: {output_path}")





def render_results_dashboard():
    """Render results dashboard"""
    st.header("📊 Migration Results Dashboard")
    
    # Overall pipeline status
    progress = st.session_state.pipeline_progress
    
    col1, col2, col3, col4, col5 = st.columns(5)  # UPDATED TO INCLUDE PROGRAM 5
    
    with col1:
        status = progress['program_1']['status']
        st.metric("Program 1", "BizTalk Mapper", delta=status.title())
    
    with col2:
        status = progress['program_2']['status']
        st.metric("Program 2", "ACE Foundation", delta=status.title())
    
    with col3:
        status = progress['program_3']['status']
        st.metric("Program 3", "ACE Module Creator", delta=status.title())
    
    with col4:
        status = progress['program_4']['status']
        st.metric("Program 4", "Quality Review", delta=status.title())
    
    with col5:  # NEW COLUMN FOR PROGRAM 5
        status = progress['program_5']['status']
        st.metric("Program 5", "Functional Docs", delta=status.title())
    
    # Show final results if all programs completed
    if all(progress[prog]['status'] == 'success' for prog in progress):
        st.success("🎉 **MIGRATION PIPELINE COMPLETED SUCCESSFULLY!**")
        
        st.subheader("📁 Generated Artifacts")
        
        # List all outputs
        artifacts = []
        for i, prog in enumerate(['program_1', 'program_2', 'program_3', 'program_4', 'program_5'], 1):
            output = progress[prog]['output']
            if output:
                artifacts.append(f"**Program {i}**: {output}")
        
        for artifact in artifacts:
            st.write(artifact)
        
        # Next steps
        st.subheader("🚀 Next Steps")
        st.markdown("""
        1. ✅ **Review** generated functional documentation
        2. ✅ **Review** generated quality reports
        3. ✅ **Import** ACE foundation into IBM ACE Toolkit
        4. ✅ **Configure** database connections and environment settings
        5. ✅ **Test** enhanced ESQL modules individually
        6. ✅ **Deploy** to ACE runtime environment
        7. ✅ **Perform** end-to-end testing
        8. ✅ **Go-live** with migrated solution
        """)
    
    elif any(progress[prog]['status'] == 'error' for prog in progress):
        st.error("❌ **PIPELINE HAS ERRORS** - Check individual program tabs for details")
    
    else:
        st.info("⏳ **PIPELINE IN PROGRESS** - Continue with remaining programs")

if __name__ == "__main__":
    main()