import os
import io
import setuptools
from pathlib import Path

def main():
    package_root = os.path.abspath(os.path.dirname(__file__))
    proot = Path(package_root)
    readme_filename = os.path.join(package_root, "README.rst")
    with io.open(readme_filename, encoding="utf-8") as readme_file:
        readme = readme_file.read()
    dependencies = [
            'bottle',
            'google-api-python-client',
            'google-auth-httplib2',
            'google-auth-oauthlib',
            'grpcio',
            'google-cloud-ndb',
            'google-cloud-storage',
            'numpy',
            'matplotlib',
            'lxml',
            'sympy'
    ]
    packages=['chcko']
    data_files = [str(x.relative_to(proot/'chcko')) for x in proot.rglob('chcko/**/*.html')]
    setuptools.setup(
        name="chcko",
        version = "0.0.1",
        description="chcko randomly parameterized exercises automatically checked (formerly mamchecker)",
        long_description=readme,
        long_description_content_type="text/x-rst",
        author="Roland Puntaier",
        author_email="roland.puntaier@gmail.com",
        url="https://github.com/chcko/chcko",
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.8",
            "Operating System :: OS Independent",
            "Topic :: Internet",
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Topic :: Education',
            'Topic :: Education :: Computer Aided Instruction (CAI)'
        ],
        packages=packages,
        package_data={'chcko': data_files},
        #namespace_packages=["chcko"],
        install_requires=dependencies,
        extras_require={},
        include_package_data=True,
        zip_safe=False,
        tests_require=['pytest', 'pytest-cov', 'mock'],
        entry_points={
          'console_scripts': ['chcko=chcko.run:main']
        }
    )

if __name__ == "__main__":
    main()
