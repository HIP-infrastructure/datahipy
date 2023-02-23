#!/usr/bin/env cwltool
  
cwlVersion: v1.2
class: CommandLineTool
baseCommand: --command=db.get
stdout: db.get.status.txt
hints:
  DockerRequirement:
    dockerPull: bids-tools:latest
inputs:  
  input_data:
    type: File
    inputBinding:
      prefix: --input_data=
      position: 2
      separate: false
      
outputs:
  db.get:
    type: stdout


# see https://www.commonwl.org/v1.1/CommandLineTool.html#InplaceUpdateRequirement
$namespaces:
  cwltool: http://commonwl.org/cwltool#