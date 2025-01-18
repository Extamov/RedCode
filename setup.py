import setuptools

setuptools.setup(
    name="redcode",
    description="A software that alerts when there is an emergency in Israel.",
    version="0.0.4",
    author="Extamov",
    license="GPL-3.0",
    packages=setuptools.find_packages("."),
    install_requires=open("requirements.txt", encoding="utf-8").read().splitlines(),
    entry_points={"console_scripts": ["redcode=redcode.__main__:entrypoint"]},
    include_package_data=True,
)
