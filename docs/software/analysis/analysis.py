import pandas as pd
import math

# Specify the path to your Excel file
file_path = 'doe.xlsx'

# Read the Excel spreadsheet
df = pd.read_excel(file_path)

# Print the DataFrame
print(df)

solvers_list = [
    "KokkosKernels",
    "PETSc",
    "PARDISO",
    "Trilinos",
    "SuperLU-Dist",
    "STRUMPACK",
    "Hypre",
    "SPARSKIT",
    "BLAS",
    "SuperLU",
    "SparsePACK",
    "LAPACK"
]
math_list = ["SAMRAI", "STK", "MFEM", "UMR", "Portage", "Tangram", "Axom", "Overlink", "METIS", "ParMETIS", "Sculpt", "libigl"] 
compilers_list = ["Kokkos", "RAJA Suite", "FleCSI", "Flang", "MPICH", "OpenMPI", "Legion", "PyKokkos", "KokkosRemoteMemorySpaces", "Fortran", "MPI", "C", "C++", "GCC", "HIP", "CUDA", "Python", "OpenMP", "Intel Compiler Suite", "LLVM", "Perl", "PyTorch", "TensorFlow", "Boost", "Intel MPI"]
system_list = ["CharlieCloud", "LDMS", "Flux", "SICM", "AppSysFusion", "GMI", "Maestro/Merlin", "Splunk", "SLURM", "VmWare", "LSF"]
visu_list = ["VTK/VTKm", "Paraview", "Visit", "Catalyst", "Conduit", "Cinema", "Ascent"]
build_list = ["Spack", "BLT", "CMake", "Ninja", "Autoconf/Automake", "gdb", "git", "Gitlab", "git-lfs", "Valgrind", "AllineaForge", "TotalView", "Caliper", "Archer", "PAPI", "KokkosTools", "CDash", "STAT"]
io_list = ["HDF5/Parallel-HDF5", "NetCDF, pNetCDF", "SEACAS", "UnifyFS", "ZFP", "HPSS, MarFS, SILO", "Exodus, yamlcpp", "GUFI, HIO, SCR, Sina/Kosh", "CGNS, libz", "DB2, Matio", "ADIOS, szip/AEC"]


# Define the mapping from scale to numerical values
scale_mapping = {
    "Low": 0,
    "Medium": 1,
    "High": 2,
    "Very High": 3
}

data_map = {
    "solvers_list": (["KokkosKernels", "PETSc", "PARDISO", "Trilinos", "SuperLU-Dist", "STRUMPACK", "Hypre", "SPARSKIT", "BLAS", "SuperLU", "SparsePACK", "LAPACK"], "Solver Libraries"),
    "math_list": (["SAMRAI", "STK", "MFEM", "UMR", "Portage", "Tangram", "Axom", "Overlink", "METIS", "ParMETIS", "Sculpt", "libigl"], "Math, Meshing, Discretization & Decomposition"),
    "compilers_list": (["Kokkos", "RAJA Suite", "FleCSI", "Flang", "MPICH", "OpenMPI", "Legion", "PyKokkos", "KokkosRemoteMemorySpaces", "Fortran", "MPI", "C", "C++", "GCC", "HIP", "CUDA", "Python", "OpenMP", "Intel Compiler Suite", "LLVM", "Perl", "PyTorch", "TensorFlow", "Boost", "Intel MPI"], "Compilers, Runtimes and Languages"),
    "system_list": (["CharlieCloud", "LDMS", "Flux", "SICM", "AppSysFusion", "GMI", "Maestro/Merlin", "Splunk", "SLURM", "VmWare", "LSF"], "System imaging, system monitoring and management"),
    "visu_list": (["VTK/VTKm", "Paraview", "Visit", "Catalyst", "Conduit", "Cinema", "Ascent"], "Visualisation And Analysis"),
    "build_list": (["Spack", "BLT", "CMake", "Ninja", "Autoconf/Automake", "gdb", "git", "Gitlab", "git-lfs", "Valgrind", "AllineaForge", "TotalView", "Caliper", "Archer", "PAPI", "KokkosTools", "CDash", "STAT"], "Build, Development and Software Eng."),
    "io_list": (["HDF5/Parallel-HDF5", "NetCDF, pNetCDF", "SEACAS", "UnifyFS", "ZFP", "HPSS, MarFS, SILO", "Exodus, yamlcpp", "GUFI, HIO, SCR, Sina/Kosh", "CGNS, libz", "DB2, Matio", "ADIOS, szip/AEC"], "IO Storage/Data management")
}

for software_list, title in data_map.values():
    print(f"Processing {title}: {software_list}")
    average_value = dict()
    # Define the reverse mapping
    reverse_mapping = {v: k for k, v in scale_mapping.items()}

    for software in software_list:
        software_columns = [column for column in df.columns if software in column]
        if software_columns:
            # Apply the mapping to the specific columns
            df[software_columns] = df[software_columns].replace(scale_mapping)
            # Ignore rows with all NaN values
            average_value[software] = df[software_columns].dropna(how='all').mean(axis=0)
            # Convert the average value back to the scale
            average_value[software] = average_value[software].round().map(reverse_mapping)
            print(f"Average value for {software}: {average_value[software]}")
            #print(f"Average value for {software}: {average_value[software]}")
            # Print the results for each column
            #for column in software_columns:
            #    print(f"Results for {column}:")
            #    print(df[column].map(reverse_mapping).dropna())
        else:
            print(f"No columns found for {software}")


    # Define the table structure
    table = {
        ("Low", "Low"): [],
        ("Low", "Medium"): [],
        ("Low", "High"): [],
        ("Low", "Very High"): [],
        ("Medium", "Low"): [],
        ("Medium", "Medium"): [],
        ("Medium", "High"): [],
        ("Medium", "Very High"): [],
        ("High", "Low"): [],
        ("High", "Medium"): [],
        ("High", "High"): [],
        ("High", "Very High"): [],
        ("Very High", "Low"): [],
        ("Very High", "Medium"): [],
        ("Very High", "High"): [],
        ("Very High", "Very High"): [],
    }

    # Fill the table with software names
    for software in software_list:
        row=dict()
        col=dict()
        ok=0
        for key, val in average_value[software].items():
            if "Likelihood" in key:
                if val in ["Very High","High","Medium","Low"]:
                    row[software]=val
                else:
                    row[software]="Low"
            if "Impact" in key:
                if val in ["Very High","High","Medium","Low"]:
                    col[software]=val
                else:
                    col[software]="Low"
        table[(row[software], col[software])].append(software)
#    print(table)        

    ## Create the AsciiDoc table
    asciidoc_table = f"""
.Likelihood-Impact Matrix for {title}
|===\n|Likelihood \\ Impact|Very High|High|Medium|Low\n
"""
    #
    for likelihood in ["Very High","High","Medium","Low"]:
        asciidoc_table += f"|{likelihood}"
        for impact in ["Very High","High","Medium","Low"]:
            asciidoc_table += f"|{', '.join(table[(likelihood, impact)])}"
        asciidoc_table += "\n"

    asciidoc_table += "|===\n\n"

    with open(f"doe-analysis.adoc", "a") as f:
        f.write(f"== {title}")
        f.write(asciidoc_table)



