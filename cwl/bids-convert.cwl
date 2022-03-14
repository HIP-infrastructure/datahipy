#!/usr/bin/env cwltool

$namespaces:
  cwltool: http://commonwl.org/cwltool#
  
cwlVersion: v1.0
class: CommandLineTool
baseCommand: python3
hints:
  DockerRequirement:
    dockerPull: bids-converter:latest
  cwltool:InplaceUpdateRequirement:
    inplaceUpdate: true
requirements:
  InitialWorkDirRequirement:
    listing:
      - entry: $(inputs.output_directory)
        writable: true
inputs:
  input_command:
    type: string
    inputBinding:
      position: 1
  input_file:
    type: File
    inputBinding:
      prefix: -create_bids_db
      position: 2
  output_directory:
    type: Directory
    inputBinding:
      prefix: --output_directory
      position: 3
outputs:
  status:
    type: stdout
stdout: status.txt
