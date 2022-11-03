from Pascal2GT import Pascal2GT


if __name__ == '__main__':

    '''
    Transform Pascal VOC xml files into a manifest file of AWS Ground Truth

    project_name: Your created labeling job name. Need to change everytime you create new job.
    s3_path: Your images location in S3. Need to change everytime you have new folder of images.
    '''

    pascal2gt = Pascal2GT(
        project_name = "labeling-job-m00", 
        s3_path = "s3://aws-jgp-ml-m00/inputs/221026-cherrypick-example")


    '''
    path_target_manifest: the path manifest being saved in this local project 
    path_source_xml_dir: the xmls directory path in this local project
    path_project_yaml_file: the project yaml file that consist of labels' name
    '''

    pascal2gt.run(
        path_target_manifest = "./221026-cherrypick-example/output.manifest", 
        path_source_xml_dir = "./221026-cherrypick-example",
        path_project_yaml_file = "./project-files/m01.yaml"
        )