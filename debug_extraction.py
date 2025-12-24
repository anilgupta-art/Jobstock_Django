"""
Debug script to test resume data extraction
Run: python debug_extraction.py
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.tasks_simple import SimpleDocumentProcessor
from pathlib import Path

def test_extraction():
    """Test extraction on existing resume files"""
    
    # Initialize processor
    processor = SimpleDocumentProcessor()
    
    # Find resume files
    resume_dir = Path("Data/resume")
    if not resume_dir.exists():
        print(f"❌ Resume directory not found: {resume_dir}")
        return
    
    resume_files = list(resume_dir.glob("*.pdf")) + list(resume_dir.glob("*.docx"))
    
    if not resume_files:
        print("❌ No resume files found in Data/resume/")
        return
    
    print("=" * 80)
    print(f"Found {len(resume_files)} resume files")
    print("=" * 80)
    
    for i, resume_file in enumerate(resume_files[:3], 1):  # Test first 3 resumes
        print(f"\n{'=' * 80}")
        print(f"TESTING RESUME {i}: {resume_file.name}")
        print("=" * 80)
        
        try:
            # Extract text
            print("\n⏳ Step 1: Extracting text...")
            text = processor.extract_text(str(resume_file))
            print(f"✅ Extracted {len(text)} characters")
            print(f"\nFirst 500 characters:")
            print("-" * 80)
            print(text[:500])
            print("-" * 80)
            
            # Extract contact info
            print("\n⏳ Step 2: Extracting contact information...")
            contact_info = processor.extract_contact_info(text)
            print(f"✅ Contact Info:")
            print(f"   📧 Emails: {contact_info['emails']}")
            print(f"   📱 Phones: {contact_info['phones']}")
            print(f"✅ Contact Info:")
            print(f"   👤 Candidate Name: {contact_info['name']}")
            print(f"   💻 GitHub: {contact_info['github']}")
            
            # Extract entities (names)
            print("\n⏳ Step 3: Extracting entities (names)...")
            entities = processor.extract_entities(text)
            print(f"✅ Entities Found:")
            print(f"   👤 Persons: {entities['persons'][:5]}")  # Show first 5
            print(f"   🏢 Organizations: {entities['organizations'][:5]}")
            print(f"   📍 Locations: {entities['locations'][:5]}")
            
            # Debug phone extraction
            if not contact_info['phones']:
                print("\n⚠️  NO PHONES FOUND - Debugging phone patterns...")
                print("Searching for phone-like patterns manually:")
                import re
                
                # More comprehensive phone patterns
                patterns = {
                    'Standard': r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
                    'With Country': r'\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
                    'Parentheses': r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',
                    'International': r'\+?\d{1,4}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
                    'Simple 10-digit': r'\b\d{10}\b'
                }
                
                for pattern_name, pattern in patterns.items():
                    matches = re.findall(pattern, text)
                    if matches:
                        print(f"   {pattern_name}: {matches[:3]}")
            
            # Debug name extraction
            if not entities['persons']:
                print("\n⚠️  NO NAMES FOUND - Debugging name extraction...")
                print("Looking for name-like patterns in first 1000 characters:")
                # Names are usually in first part of resume
                first_part = text[:1000]
                print(first_part)
                
        except Exception as e:
            print(f"❌ Error processing {resume_file.name}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("DEBUGGING COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_extraction()
