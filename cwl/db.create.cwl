#!/usr/bin/env cwltool
  
cwlVersion: v1.2
class: CommandLineTool
baseCommand: --command=db.create
stdout: db.create.status.txt
hints:
  DockerRequirement:
    dockerPull: bids-tools:latest
  # This doesn't work anymore
  # https://github.com/common-workflow-language/cwltool/issues/993
  # Should allow the db to be edited in place
  cwltool:InplaceUpdateRequirement:
    inplaceUpdate: true
requirements:
  InitialWorkDirRequirement:
    listing:
      - entry: $(inputs.database_path)
        writable: true
inputs:  
  input_data:
    type: File
    inputBinding:
      prefix: --input_data=
      position: 2
      separate: false
  
  database_path:
    type: Directory?
    inputBinding:
      prefix: --database_path=
      position: 3
      separate: false
      
outputs:
  db.create:
    type: stdout


# see https://www.commonwl.org/v1.1/CommandLineTool.html#InplaceUpdateRequirement
$namespaces:
  cwltool: http://commonwl.org/cwltool#