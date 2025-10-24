"""
Script to create a deployment package for the Clinic Management System
This will create a ZIP file ready to send to the client
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_deployment_package():
    print("="*60)
    print("Creating Clinic Management System Deployment Package")
    print("="*60)
    
    # Package name with date
    date_str = datetime.now().strftime("%Y%m%d")
    package_name = f"ClinicManagementSystem_{date_str}"
    package_dir = f"package_{package_name}"
    
    # Create package directory
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    print(f"\n📦 Creating package: {package_name}")
    
    # Files and folders to include
    items_to_copy = [
        'app.py',
        'models.py',
        'forms.py',
        'seed.py',
        'requirements.txt',
        'templates',
        'static',
        'run_clinic.bat',
        'INSTALLATION_GUIDE.txt',
        'QUICK_START.txt',
        'README.md'
    ]
    
    print("\n📋 Copying files...")
    for item in items_to_copy:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.copytree(item, os.path.join(package_dir, item))
                print(f"  ✓ Copied folder: {item}")
            else:
                shutil.copy2(item, package_dir)
                print(f"  ✓ Copied file: {item}")
        else:
            print(f"  ⚠ Skipped (not found): {item}")
    
    # Create empty instance directory
    instance_dir = os.path.join(package_dir, 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    print(f"  ✓ Created: instance/ (empty)")
    
    # Create a README in the instance folder
    with open(os.path.join(instance_dir, 'README.txt'), 'w') as f:
        f.write("This folder will contain your clinic database (clinic.db)\n")
        f.write("IMPORTANT: Backup this folder regularly!\n")
        f.write("The database file will be created automatically on first run.\n")
    
    # Create ZIP file
    zip_filename = f"{package_name}.zip"
    print(f"\n📦 Creating ZIP file: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
                
    # Clean up temporary package directory
    shutil.rmtree(package_dir)
    
    # Get file size
    file_size = os.path.getsize(zip_filename) / (1024 * 1024)  # Convert to MB
    
    print("\n" + "="*60)
    print("✅ PACKAGE CREATED SUCCESSFULLY!")
    print("="*60)
    print(f"\n📦 Package file: {zip_filename}")
    print(f"📏 File size: {file_size:.2f} MB")
    print(f"\n📂 Location: {os.path.abspath(zip_filename)}")
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Send the ZIP file to your client")
    print("2. Tell them to:")
    print("   - Extract the ZIP file")
    print("   - Read QUICK_START.txt")
    print("   - Double-click run_clinic.bat")
    print("   - Open browser to http://127.0.0.1:5000")
    print("\n" + "="*60)
    
    return zip_filename

if __name__ == "__main__":
    try:
        zip_file = create_deployment_package()
        print("\n✨ All done! Package is ready to send.")
    except Exception as e:
        print(f"\n❌ Error creating package: {e}")
        import traceback
        traceback.print_exc()

