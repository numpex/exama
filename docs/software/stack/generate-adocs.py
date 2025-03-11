import pandas as pd
import os
df = pd.read_excel('software.xlsx')
df_packaging = pd.read_excel('software.xlsx', sheet_name='Packaging')

def generate_asciidoc(row,packaging_row):
    adoc = f"= {row['Name']} Package\n\n"
    print(f"using packaging row: {packaging_row}")
    description = row.get('Description', '') or ''
    description = description.strip() if pd.notnull(description) else ''

    devops = str(row.get('DevOps', '') or '')
    license_info = str(row.get('License', '') or '')
    repository = str(row.get('Repository', '') or '')
    docs = str(row.get('Docs', '') or '').strip()
    channels = str(row.get('Channels', '') or '').strip()
    apis = str(row.get('API', '') or '').lower()

    # packaging info
    package_spack = packaging_row.get('Spack Info Source', '') or ''
    package_spack = package_spack.strip() if pd.notnull(package_spack) else ''
    package_guix = packaging_row.get('Guix-HPC Info Source', '') or ''
    package_guix = package_guix.strip() if pd.notnull(package_guix) else ''
    package_petsc = packaging_row.get('PETSc Info Source', '') or ''
    package_petsc = package_petsc.strip() if pd.notnull(package_petsc) else ''
    package_docker = packaging_row.get('Docker Info Source', '') or ''
    package_docker = package_docker.strip() if pd.notnull(package_docker) else ''
    package_apptainer = packaging_row.get('Apptainer Info Source', '') or ''
    package_apptainer = package_apptainer.strip() if pd.notnull(package_apptainer) else ''

    adoc += f"== Description\n\n"
    if description:
        adoc += f"{description if description else 'No description provided.'}\n\n"
    else:
        adoc += "No description provided.\n\n"

    adoc += "== Packaging\n\n"
    adoc += "Software should be packaged (preferably using Spack or Guix package formats). They should be published in public (community controlled) package repositories (Guix-science, etc.).\n\n"
    adoc += f"* [{'x' if 'Packages' in devops else ' '}] Packages exist\n"
    adoc += f"* [{'x' if any(repo in devops for repo in ['Spack', 'GUIX', 'Debian', 'Ubuntu', 'Fedora']) else ' '}] Packages published in easily usable repositories\n"
    adoc += f"* [{'x' if 'supercomputers' in devops.lower() else ' '}] Packages installation tested on supercomputers\n"
    adoc += f"* [{'x' if any(c in devops for c in ['Spack', 'GUIX']) else ' '}] Packages available in community repositories\n\n"
    if package_spack:
        print(f"Package Spack: {package_spack}")
        adoc += f"  - Spack: {package_spack}\n"
    if package_guix:
        adoc += f"  - Guix: {package_guix}\n"
    if package_petsc:
        adoc += f"  - PETSc: {package_petsc}\n"
    if package_docker:
        adoc += f"  - Docker: {package_docker}\n"
    if package_apptainer:
        adoc += f"  - Apptainer: {package_apptainer}\n"

    # Extracting all packaging types from 'devops'
    package_types = [pkg.strip().replace('Packages - ', '')
                     for pkg in devops.split(',') if 'Packages -' in pkg]

    if package_types:
        adoc += "\nAvailable packages:\n\n"
        for pkg in package_types:
            adoc += f"- {pkg}\n"        
    adoc += "\n"

    adoc += "== Minimal Validation Tests\n\n"
    adoc += "Software should include minimal validation tests triggered through automated mechanism such as Guix. These tests should be automatic functional tests that do not require specific hardware.\n\n"
    adoc += f"* [{'x' if 'Test - Unit' in devops else ' '}] Unit tests exist\n"
    adoc += f"* [{'x' if 'Continuous Integration' in devops else ' '}] CI exists\n"
    adoc += f"* [{'x' if 'Continuous Delivery' in devops else ' '}] CI runs regularly (each new release)\n"
    adoc += f"* [{'x' if 'Continuous Integration' in devops else ' '}] CI runs regularly (each commit)\n\n"

    adoc += "== Public Repository\n\n"
    adoc += "A public repository, must be available for at least the development version of the software, allowing for pull requests to be submitted.\n\n"
    adoc += f"* [{'x' if repository else ' '}] Publicly available source repository\n"
    adoc += f"* [{'x' if 'github.com' in repository.lower() or 'gitlab' in repository.lower() else ' '}] Supports contribution via pull requests\n"
    if repository:
        adoc += f"\nRepository: {repository}\n\n"

    adoc += "== Clearly-identified license\n\n"
    adoc += "Sources should be published under a clearly-identified free software license (preferably with REUSE)\n\n"
    adoc += f"* [{'x' if license_info else ' '}] License clearly stated\n"
    adoc += f"* [{'x' if any(l in license_info for l in ['GPL', 'LGPL', 'MIT', 'BSD', 'Apache']) else ' '}] FLOSS license (FSF/OSI conformant)\n"
    adoc += "* [ ] SPDX is used\n"
    adoc += "* [ ] REUSE is used\n\n"
    if license_info:
        for lic in license_info.split(','):
            adoc += f"  - {lic.strip()}\n"
    adoc += "\n"

    adoc += "== Minimal Documentation\n\n"
    adoc += "Basic documentation should be publicly available to facilitate user understanding and usage of the software.\n\n"
    adoc += f"* [{'x' if docs else ' '}] Documentation exists\n"
    adoc += f"* [{'x' if docs.startswith('https://') else ' '}] Easily browsable online\n"
    if docs:
        for doc in docs.split(','):
            adoc += f"  - {doc.strip()}\n"
    adoc += "\n"

    adoc += "== Open Public Discussion Channel\n\n"
    adoc += "An open, public discussion channel must be provided that is easily accessible to all potential users. The chosen platform must not require special permissions or memberships that could limit user participation.\n\n"
    adoc += f"* [{'x' if channels else ' '}] Channel exists\n"
    adoc += f"* [{'x' if channels else ' '}] Freely joinable without invitation\n"
    if channels:
        for channel in channels.split(','):
            adoc += f"  - {channel.strip()}\n"
    adoc += "\n"

    adoc += "== Metadata\n\n"
    adoc += "Each repository should include metadata easing integration and publicity on a software list.\n\n"
    metadata_fields = {
        "Software name": row.get('Name'),
        "Description": row.get('Description'),
        "License": row.get('License'),
        "Documentation URL": row.get('Docs'),
        "Discussion channel URL": row.get('Channels'),
        "Package repositories URLs": row.get('DevOps'),
        "Repository URL": row.get('Repository'),
        "Autoevaluation using the list of criteria stated here": 'Yes'
    }

    all_metadata_available = all(pd.notnull(val) and str(val).strip() for val in metadata_fields.values())

    adoc += f"* [{'x' if all_metadata_available else ' '}] The following metadata is available:\n"
    for key, val in metadata_fields.items():
        status = '✅' if pd.notnull(val) and str(val).strip() else '❌'
        adoc += f"  - {key}: {status}\n"
    adoc += "\n"

    codemeta_present = 'codemeta' in devops.lower()
    adoc += f"* [{'x' if codemeta_present else ' '}] Uses codemeta format\n\n"

    adoc += "== API Compatibility Information\n\n"
    adoc += "Each repository should include information enabling downstream users to know which versions they can use\n\n"
    adoc += f"* [{'x' if 'api changes documented' in apis else ' '}] API changes documented\n"
    adoc += f"* [{'x' if 'semantic versioning' in apis else ' '}] Semantic Versioning used\n"
    adoc += f"* [{'x' if 'release policy' in apis else ' '}] Clear release policy\n\n"

    adoc += "== Minimal Performance Tests\n\n"
    adoc += "Software should include a minimal set of performance tests divided in three categories: single node without specific hardware, single node with specific hardware, multi-nodes. These tests should be automated as much as possible.\n\n"
    adoc += f"* [{'x' if ('unit' in devops.lower() or 'verification' in devops.lower()) else ' '}] Tests exist\n"
    adoc += f"* [{'x' if 'benchmarking' in devops.lower() else ' '}] Scripts to automate tests on supercomputers\n"
    adoc += "* [ ] Scripts/tools easing portability to new hardware\n\n"

    return adoc

nav_entries = []

for index, row in df.iterrows():
    packaging_row = df_packaging.iloc[index]
    benchmarked = pd.notnull(row.get('Benchmarked')) and str(row['Benchmarked']).strip().upper()
    licensed = pd.notnull(row.get('License')) and str(row['License']).strip()
    packaged = pd.notnull(row.get('DevOps')) and str(row['DevOps']).strip()
    if benchmarked and benchmarked != 'NOT YET' and licensed and packaged:
        print(f"Generating asciidoc for {row['Name']}...")
        asciidoc = generate_asciidoc(row,packaging_row)
        filename = f"../../modules/software/pages/{row['Name'].lower().replace('/', '_').replace('+', 'p').replace(' ', '_')}.adoc"
        with open(filename, 'w') as file:
            file.write(asciidoc)
        print(f"Generated {filename}")

        # Create nav entry
        nav_entries.append(f"** xref:{filename}[{row['Name']}]")
    else:
        print(f"Skipped {row['Name']} (criteria not met)")

print("AsciiDoc files generated successfully!")

# Generate nav.adoc for Antora
nav_adoc = os.path.join('.', 'nav.adoc')
with open(nav_adoc, 'w') as nav_file:
    nav_file.write("* Software Packages\n")
    for entry in nav_entries:
        nav_file.write(f"{entry}\n")

print(f"Navigation file generated at {nav_adoc}")