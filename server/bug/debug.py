def debug_imports():
    import sys
    import os
    
    print("Python version:", sys.version)
    print("\nPython executable:", sys.executable)
    print("\nPYTHONPATH:")
    for path in sys.path:
        print(f"  - {path}")
    
    print("\nCurrent working directory:", os.getcwd())
    
    print("\nInstalled packages:")
    import pkg_resources
    installed_packages = [f"{dist.key} ({dist.version})"
                         for dist in pkg_resources.working_set]
    for package in sorted(installed_packages):
        print(f"  - {package}")

# Usage
debug_imports()

if __name__ == "__main__":
    try:
        import flask
        print("Flask is installed")
    except ModuleNotFoundError:
        print(" Flask not found! Running debug info...\n")
        debug_imports()