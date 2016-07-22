import opentargets.model.core as opentargets
import opentargets.model.bioentity as bioentity
import opentargets.model.evidence.phenotype as evidence_phenotype
import opentargets.model.evidence.core as evidence_core
import opentargets.model.evidence.linkout as evidence_linkout
import opentargets.model.evidence.association_score as association_score
import opentargets.model.evidence.mutation as evidence_mutation
import json
import sys
import logging
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
    obj = opentargets.Literature_Curated(type='genetic_literature')
    provenance_type = evidence_core.BaseProvenance_Type(
            database=evidence_core.BaseDatabase(
                id="Gene2Phenotype",
                version='2016.06',
                dbxref=evidence_core.BaseDbxref(url="http://www.ebi.ac.uk/gene2phenotype/gene2phenotype-webcode/cgi-bin/handler.cgi", id="Gene2Phenotype", version="2016.06")))
    obj.access_level = "public"
    obj.sourceID = "gene2phenotype"
    obj.validated_against_schema_version = "1.2.3"
    obj.unique_association_fields = {"target": target, "disease_uri": disease, "source_id": "gene2phenotype"}
    obj.target = bioentity.Target(id=[target], 
                                  activity="http://identifiers.org/cttv.activity/unknown", 
                                  target_type='http://identifiers.org/cttv.target/gene_evidence',
                                  target_name=symbol)
    # http://www.ontobee.org/ontology/ECO?iri=http://purl.obolibrary.org/obo/ECO_0000204 -- An evidence type that is based on an assertion by the author of a paper, which is read by a curator. 
    resource_score = association_score.Probability(
                        type="NA",
                        method= association_score.Method(
                            description ="NA", 
                            reference = "NA",
                            url = "NA"),
                        value=1)
   
    obj.disease = bioentity.Disease(id=[disease], name=[name])
    obj.evidence = evidence_core.Literature_Curated()
    obj.evidence.is_associated = True
    obj.evidence.evidence_codes = ["http://purl.obolibrary.org/obo/ECO_0000204"]
    obj.evidence.provenance_type = provenance_type
    obj.evidence.date_asserted = '2016-07-21'
    obj.evidence.provenance_type = provenance_type
    obj.evidence.resource_score = resource_score
    linkout = evidence_linkout.Linkout(
                        url = 'http://www.ebi.ac.uk/gene2phenotype/gene2phenotype-webcode/cgi-bin/handler.cgi?panel=ALL&search_term=%s' % (symbol,),
                        nice_name = 'Gene2Phenotype%s' % (symbol))
    obj.evidence.urls = [ linkout ]
    error = obj.validate(logging)
    if error > 0:
    	logging.error(obj.to_JSON())
    	sys.exit(1)
    print obj.to_JSON(indentation=None)
