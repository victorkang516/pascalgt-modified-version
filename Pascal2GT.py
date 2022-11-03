import datetime
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List
import yaml


class Pascal2GT:
    """
    Transform PASCAL-VOC xml files into ground truth
    """

    def __init__(self, project_name: str, s3_path: str):
        self.project_name = project_name
        self.s3_path = s3_path  # s3 key of the directory including images
    

    def read_project_yaml_file(self, path_project_yaml_file: str):
        # read project labels yaml file
        with open(str(path_project_yaml_file), "r") as stream:
            try:
                out = yaml.safe_load(stream)
                list_of_label_names = out['names']
            except yaml.YAMLError as exc:
                print(exc)
        
        return list_of_label_names
        


    def run(self, path_target_manifest: str, path_source_xml_dir: str, path_project_yaml_file: str):
        path_source_xml_dir = Path(path_source_xml_dir)

        files = path_source_xml_dir.glob('**/*.xml')

        list_xml = []

        for filename in files:
            xml = self.read_pascal_xml(filename)
            list_xml.append(xml)
        
        list_of_label_names = self.read_project_yaml_file(path_project_yaml_file)

        output_manifest_text = self.aggregate_xml(list_xml, list_of_label_names)

        with open(str(path_target_manifest), mode='w') as f:
            f.write(output_manifest_text)
        return


    def read_pascal_xml(self, path_xml: Path) -> ET.Element:
        assert path_xml.exists()
        xml = ET.parse(str(path_xml))
        return xml


    def aggregate_xml(self, list_xml: List[ET.Element], list_of_label_names) -> str:
        """
        aggregate list of xml structure objects into one output.manifest text.
        """
        outputText = ""
        list_output_json_dict = []
        class_name2class_id_mapping = {}

        for label_name in list_of_label_names:
            if class_name2class_id_mapping.get(label_name) is None:
                class_name2class_id_mapping[label_name] = len(class_name2class_id_mapping)

        for xml in list_xml:
            output_dict = {}

            folder = xml.find("folder").text
            filename = xml.find("filename").text
            size_object = xml.find("size")
            image_height = int(size_object.find("height").text)
            image_width = int(size_object.find("width").text)
            image_depth = int(size_object.find("depth").text)

            output_dict["source-ref"] = f"{self.s3_path}/{filename}"
            output_dict[self.project_name] = {"image_size": [{"width": image_width,
                                                            "height": image_height,
                                                            "depth": image_depth}],
                                            "annotations": []}
            output_dict[f"{self.project_name}-metadata"] = {"objects": [],
                                                            "class-map": {},
                                                            "type": "groundtruth/object-detection",
                                                            "human-annotated": "yes",
                                                            "creation-date": datetime.datetime.now().isoformat(
                                                                timespec='microseconds'),
                                                            "job-name": f"labeling-job/{self.project_name}"}

            objects = xml.findall("object")

            for annotated_object in objects:
                class_name = annotated_object.find("name").text
                if class_name2class_id_mapping.get(class_name) is None:
                    class_name2class_id_mapping[class_name] = len(class_name2class_id_mapping)

                class_id = class_name2class_id_mapping[class_name]

                bbox_object = annotated_object.find("bndbox")
                x1 = int(bbox_object.find("xmin").text)
                x2 = int(bbox_object.find("xmax").text)
                y1 = int(bbox_object.find("ymin").text)
                y2 = int(bbox_object.find("ymax").text)
                bbox_width = x2 - x1
                bbox_height = y2 - y1

                output_dict[self.project_name]["annotations"].append(
                    {
                        "class_id": class_id,
                        "top": y1,
                        "left": x1,
                        "height": bbox_height,
                        "width": bbox_width,
                    }
                )
                output_dict[f"{self.project_name}-metadata"]["objects"].append({"confidence": 0})

            list_output_json_dict.append(output_dict)

        for output_dict in list_output_json_dict:
            output_dict[f"{self.project_name}-metadata"]["class-map"] = {str(class_id): str(class_name) for (class_name, class_id) in class_name2class_id_mapping.items()}
            outputText += json.dumps(output_dict, separators=(",", ":")) + "\n"
        return outputText
