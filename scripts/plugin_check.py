import importlib.metadata

def check_requirements(requirements_file):
    with open(requirements_file, 'r') as file:
        dependencies = file.read().splitlines()
    
    for dependency in dependencies:
        package_name = dependency.split('==')[0]
        try:
            version = importlib.metadata.version(package_name)
            print(f"{dependency} is installed as required.")
        except importlib.metadata.PackageNotFoundError:
            print(f"{dependency} is NOT installed, please install it mannually.")

check_requirements('requirements.txt')
