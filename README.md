# pascalgt-modified-version

Original script:
https://github.com/DaikiTanak/pascalgt

# What have been modified in this script

<h2>Read all files under the path hierachy</h2>

```
files = path_source_xml_dir.glob('**/*.xml')
```

<h2>Read list of class_name (labels) from a yaml file </h2>

```
pascal2gt.run(
    path_target_manifest = "./221026-example-images/output.manifest", 
    path_source_xml_dir = "./221026-example-images",
    path_project_yaml_file = "./project-files/project01.yaml"
)
```
