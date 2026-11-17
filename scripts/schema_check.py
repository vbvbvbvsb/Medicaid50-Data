"""Dependency-free validator for the assertion keywords used by this schema. MIT licensed."""
import re

def validate_schema(value, schema, root=None, path='$'):
    """Validate all assertion keywords used by the repository's JSON Schema, dependency-free.

    Fail closed if that schema introduces an unsupported keyword in a future release.
    """
    root = schema if root is None else root
    known={'$schema','title','description','$defs','$ref','type','required','properties','additionalProperties','enum','pattern','minItems','maxItems','items'}
    assert not set(schema)-known, ('Unsupported schema keywords',set(schema)-known)
    if '$ref' in schema:
        target=root
        for part in schema['$ref'].split('/')[1:]:target=target[part]
        validate_schema(value,target,root,path)
    types={'object':dict,'array':list,'string':str,'null':type(None)}
    if 'type' in schema:
        ts=schema['type'] if isinstance(schema['type'],list) else [schema['type']]
        assert any(type(value) is types[t] for t in ts),(path,'type')
    if 'enum' in schema: assert value in schema['enum'],(path,'enum')
    if 'pattern' in schema and isinstance(value,str):assert re.search(schema['pattern'],value),(path,'pattern')
    if isinstance(value,list):
        assert len(value)>=schema.get('minItems',0),(path,'minItems')
        assert len(value)<=schema.get('maxItems',len(value)),(path,'maxItems')
        for i,v in enumerate(value):
            if 'items' in schema:validate_schema(v,schema['items'],root,f'{path}[{i}]')
    if isinstance(value,dict):
        assert all(k in value for k in schema.get('required',[])),(path,'required')
        props=schema.get('properties',{})
        for k,v in value.items():
            if k in props:validate_schema(v,props[k],root,path+'.'+k)
            elif schema.get('additionalProperties') is False:raise AssertionError((path,k,'additionalProperties'))
            elif isinstance(schema.get('additionalProperties'),dict):validate_schema(v,schema['additionalProperties'],root,path+'.'+k)

