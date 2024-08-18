from SPARQLWrapper import SPARQLWrapper
from pydantic import BaseModel
from fastapi import FastAPI
from rdfproxy import SPARQLModelAdapter
from typing import Optional, Any

app = FastAPI()

query = """
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
SELECT ?itemLabel ?occupationLabel
WHERE
{
  ?item wdt:P31 wd:Q18544860.
  OPTIONAL { ?item wdt:P106 ?occupation } .
  OPTIONAL { ?item wdt:P21 ?gender } .
  OPTIONAL { ?item wdt:P735 ?givenName } .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
"""


class DiscworldCharacter(BaseModel):
    itemLabel: Optional[str]
    occupationLabel: Optional[str] = None
    genderLabel: Optional[str] = None


sparqlwrapper = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
adapter = SPARQLModelAdapter(sparql_wrapper=sparqlwrapper)


@app.get("/")
def base():
    return adapter(query=query, model_constructor=DiscworldCharacter)
