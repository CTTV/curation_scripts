from cttv.model.core import *
import cttv.model.evidence.core as evidence
import cttv.model.evidence.association_score as evidence_score
import json
import sys

'''
Extracted input JSONs from Postgres with the following command
psql -h localhost -d cttv_core_test -p 5432 -U tvdev -A -F $'\t' -X -t -c "SELECT JSON_BUILD_OBJECT('disease', disease, 'target', target, 'disease_label', disease_label, 'gene_symbol', gene_symbol) FROM gene2phenotype.final_data_for_evstrs_jul2016" >final_data_for_evstrs_jul2016.json
This is a skeleton only, need to add fields for score and evidence codes.
'''
source_file = sys.argv[1]

for doc_json in open(source_file, 'r'):
    doc_ds = json.loads(doc_json)
    (target, disease, name, symbol) = (doc_ds['target'], 
						               doc_ds['disease'],
						               doc_ds['disease_label'],
						               doc_ds['gene_symbol'])
    obj = Literature_Curated(type='curated')
    obj.access_level = "public"
    obj.sourceID = "gene2phenotype"
    obj.validated_against_schema_version = "1.2.3"
    obj.unique_association_fields = {"target": target, "disease_uri": disease, "source_id": "gene2phenotype"}
    obj.target = bioentity.Target(id=[target], 
                                  activity="http://identifiers.org/cttv.activity/up_or_down", 
                                  target_type='http://identifiers.org/cttv.target/gene_evidence',
                                  target_name=symbol)
    obj.evidence = evidence.type = "genetics_literature"
    # http://www.ontobee.org/ontology/ECO?iri=http://purl.obolibrary.org/obo/ECO_0000204 -- An evidence type that is based on an assertion by the author of a paper, which is read by a curator.
    obj.disease = bioentity.Disease(id=[disease], name=[name])
    obj.evidence = evidence.Literature_Curated()
    obj.evidence.provenance_type = evidence.BaseProvenance_Type()
    obj.evidence.evidence_codes = ["http://purl.obolibrary.org/obo/ECO_0000204"]
    obj.evidence.date_asserted = '2016-07-21'
    print obj.to_JSON(indentation=None)
