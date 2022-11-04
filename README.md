# pascalgt-modified-version

Original script:
https://github.com/DaikiTanak/pascalgt

# What have been modified in this script

Read all files under the path hierachy

```
files = path_source_xml_dir.glob('**/*.xml')
```

Read list of class_name (labels) from a yaml file

```
pascal2gt.run(
    path_target_manifest = "./221026-example-images/output.manifest", 
    path_source_xml_dir = "./221026-example-images",
    path_project_yaml_file = "./project-files/project01.yaml"
)
```
