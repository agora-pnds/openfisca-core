# -*- coding: utf-8 -*-

import itertools

from . import conv


def parse_entities(test_case, tax_benefit_system, state):

    def build_role_parser(role):
            if role.max == 1:
                return conv.test_isinstance((basestring, int))
            else:
                return conv.pipe(
                    conv.make_item_to_singleton(),
                    conv.test_isinstance(list),
                    conv.uniform_sequence(
                        conv.test_isinstance((basestring, int)),
                        drop_none_items = True,
                        ),
                    conv.default([]),
                    )


    def get_role_parsing_dict(entity):
        if entity.is_person:
            return {}
        else:
            return {
                role.plural: build_role_parser(role)
                for role in entity.roles
            }


    def get_entity_parsing_dict(tax_benefit_system):
        column_by_name = tax_benefit_system.column_by_name
        return {
            entity.plural : conv.pipe(
                        conv.make_item_to_singleton(),
                        conv.test_isinstance(list),
                        conv.uniform_sequence(
                            conv.test_isinstance(dict),
                            drop_none_items = True,
                            ),
                        conv.function(set_entities_json_id),
                        conv.uniform_sequence(
                            conv.struct(
                                dict(itertools.chain(
                                    dict(
                                        id = conv.pipe(
                                            conv.test_isinstance((basestring, int)),
                                            conv.not_none,
                                            ),
                                        ).iteritems(),
                                    get_role_parsing_dict(entity).iteritems(),
                                    (
                                        (column.name, column.json_to_python)
                                        for column in column_by_name.itervalues()
                                        if column.entity == entity
                                        ),
                                    )),
                                drop_none_values = True,
                                ),
                            drop_none_items = True,
                            ),
                        conv.default([]),
                        )
            for entity in tax_benefit_system.entities
        }


    test_case, error = conv.pipe(
    conv.test_isinstance(dict),
    conv.struct(get_entity_parsing_dict(tax_benefit_system)),
    )(test_case, state = state)

    return test_case, error


def set_entities_json_id(entities_json):
    for index, entity_json in enumerate(entities_json):
        if 'id' not in entity_json:
            entity_json['id'] = index
    return entities_json
