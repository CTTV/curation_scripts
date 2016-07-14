from cttv.model.core import *
import cttv.model.evidence.core as evidence
import cttv.model.evidence.association_score as evidence_score
import json
import sys

'''
Extracted input JSONs from Postgres with the following command
psql -h localhost -d cttv_core_test -p 5432 -U tvdev -A -F $'\t' -X -t -c "SELECT JSON_BUILD_OBJECT('disease', disease, 'target', target) FROM gene2phenotype.final_data_for_evstrs_jul2016" >final_data_for_evstrs_jul2016.json
This is a skeleton only, need to add fields for score and evidence codes.
'''
source_file = sys.argv[1]

for doc_json in open(source_file, 'r'):
    doc_ds = json.loads(doc_json)
    (target, disease) = (doc_ds['target'], 
						doc_ds['disease'])
    obj = Literature_Mining(type='curated')
    obj.access_level = "public"
    obj.sourceID = "gene2phenotype"
    obj.validated_against_schema_version = "1.2.1"
    obj.unique_association_fields = {"target": target, "disease_uri": disease}
    obj.target = bioentity.Target(id=[target], activity="http://identifiers.org/cttv.activity/up_or_down", target_type="http://identifiers.org/cttv.target/gene_or_protein_or_transcript")
    obj.disease = bioentity.Disease(id=[disease])
    obj.evidence = evidence.Literature_Curated()
    obj.evidence.provenance_type = evidence.BaseProvenance_Type()
    obj.evidence.date_asserted = '2016-07-14'
    print obj.to_JSON(indentation=None)
