from pathlib import Path
import json,subprocess
r=Path('/workspace/work/mecha-impact-v003');s=(r/'ask.py').read_text().replace('WIDE=(2048,1024)','WIDE=(2304,1024)');(r/'ask-wide.py').write_text(s);p=json.loads((r/'plan.json').read_text())
for q in p:
 if q['group']!='palm':continue
 q['request']=str(r/'requests-wide'/q['id']);q['reference_canvas']=[2304,1024]
 subprocess.run(['python',str(r/'ask-wide.py'),'ask-view','--master','/workspace/work/mecha-impact-v002/ask-28/master.png','--cell','8','--key','green','--view-words',q['pose'],'--output-dir',q['request']],capture_output=True,check=True)
(r/'plan.json').write_text(json.dumps(p,indent=2));(r/'extract.py').write_text("from pathlib import Path\nimport subprocess,sys,json\nr=Path('/workspace/work/mecha-impact-v003');id=sys.argv[1];source=sys.argv[2];row=next(q for q in json.loads((r/'plan.json').read_text()) if q['id']==id)\nsubprocess.run(['python',str(r/'read.py'),'view','--image',source,'--request',row['request'],'--name','pose-'+id,'--output-dir',str(r/f'extracted-{id}')],check=True)\n")
