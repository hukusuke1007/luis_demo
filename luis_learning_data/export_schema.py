#!/usr/bin/env python3

import json
import csv
from collections import defaultdict, OrderedDict

def main():
    df = _read_csv('./input.csv')
    output = _create_output(df)
    print(json.dumps(output))


class DataFrame(list):
    def __getitem__(self, key: str) -> list:
        return [x[key] for x in self]

    def keys(self) -> set:
        res = set()
        for x in self:
            for y in x.keys():
                res.add(y)
        return res


def _create_output(df: DataFrame) -> OrderedDict:
    entity_keys = df.keys() - {'text', 'Entities', 'intent'}
    entities = _create_entities(entity_keys)
    intents = _create_intents(df['intent'])
    utterrances = _create_utterances(df, entity_keys)
    return _create_luis_schema(intents, entities, utterrances)


def _read_csv(path: str) -> DataFrame:
    with open(path, 'r', encoding='shift-jis') as f:
    # with open(path, 'r', encoding='utf-8') as f:
        df = DataFrame(l for l in csv.DictReader(f) if l)
    return df    


def _create_entities(entities: list) -> list:
    res = []
    for name, children in _parse_entities(entities).items():
        cs = [c for c in children if c is not None]
        res.append(_create_entity(name, cs))
    return res


def _create_intents(intents: list) -> list:
    res = set(intents)
    res.add('None')
    return [{'name': n} for n in res]


def _parse_entities(entities: list) -> defaultdict(set):
    res = defaultdict(set)
    for entity in entities:
        name, child = _parse_entity(entity)
        res[name].add(child)
    return res


def _parse_entity(entity: str) -> tuple:
    if '::' not in entity:
        return (entity, None)
    return tuple(entity.split('::'))


def _create_entity(name: str, children: set) -> OrderedDict:
    res = OrderedDict([('name', name), ('roles', [])])
    if len(children) >= 1:
        res['children'] = list(children)
    return res


def _create_utterances(rows: DataFrame, entity_keys) -> list:
    return [_create_utterrance(x, entity_keys) for x in rows]


def _create_utterrance(row: dict, entity_keys: set) -> OrderedDict:
    return OrderedDict([
      ('text', row['text']),
      ('intent', row['intent']),
      ('entities', _create_utterrance_entities(
          row['text'], [(k, row[k]) for k in entity_keys]))
    ])


def _create_utterrance_entities(text: str, entitity_items: list) -> list:
    return [_create_utterrance_entity(text, k, v)
            for k, v in entitity_items if v]  # not ''


def _create_utterrance_entity(text: str, entity_key: str, entity_value: str) -> OrderedDict:
    start_pos = text.find(entity_value)
    return OrderedDict([
        ('entity', entity_key),
        ('startPos', start_pos),
        ('endPos', start_pos + len(entity_value) - 1)
    ])


def _create_luis_schema(
        intents: list, entities: list, utterrances: list) -> OrderedDict:
    return OrderedDict([
        ('luis_schema_version', '3.0.0'),
        ('versionId', '0.1'),
        ('name', 'AutoLine'),
        ('desc', 'forTestOperator'),
        ('culture', 'ja-jp'),
        ('intents', intents),
        ('entities', entities),
        ('composites', []),
        ('closedLists', []),
        ('patternAnyEntities', []),
        ('regex_entities', []),
        ('prebuiltEntities', []),
        ('model_features', []),
        ('regex_features', []),
        ('patterns', []),
        ('utterances', utterrances)
    ])


if __name__ == '__main__':
    main()