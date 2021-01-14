pipeline = [
    {
        '$addFields': {
            'datetime': {
                '$toDate': {
                    '$multiply': [
                        '$counted_at', 1000
                    ]
                }
            }
        }
    }, {
        '$addFields': {
            'counted_at': {
                '$convert': {
                    'input': '$counted_at',
                    'to': 'double',
                    'onError': None
                }
            },
            'computer_id': {
                '$convert': {
                    'input': '$computer_id',
                    'to': 'string',
                    'onError': None
                }
            }
        }
    }, {
        '$match': {
            'arg_file': {
                '$in': [
                    'jackson_hole.env'
                ]
            },
            'type': {
                '$nin': []
            },
            'computer_id': {
                '$in': [
                    None, '', '00000000-0000-0000-0000-3cecef225486', '00000000-0000-0000-0000-f894c218ae25'
                ]
            },
        }
    }, {
        '$addFields': {
            'datetime': {
                '$cond': {
                    'if': {
                        '$eq': [
                            {
                                '$type': '$datetime'
                            }, 'date'
                        ]
                    },
                    'then': '$datetime',
                    'else': None
                }
            }
        }
    }, {
        '$addFields': {
            '__alias_0': {
                'year': {
                    '$year': '$datetime'
                },
                'month': {
                    '$subtract': [
                        {
                            '$month': '$datetime'
                        }, 1
                    ]
                },
                'date': {
                    '$dayOfMonth': '$datetime'
                },
                'hours': {
                    '$hour': '$datetime'
                },
                'minutes': {
                    '$minute': '$datetime'
                }
            }
        }
    }, {
        '$group': {
            '_id': {
                '__alias_0': '$__alias_0'
            },
            '__alias_1': {
                '$sum': {
                    '$cond': [
                        {
                            '$ne': [
                                {
                                    '$type': '$datetime'
                                }, 'missing'
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    }, {
        '$project': {
            '_id': 0,
            '__alias_0': '$_id.__alias_0',
            '__alias_1': 1
        }
    }, {
        '$project': {
            'x': '$__alias_0',
            'y': '$__alias_1',
            '_id': 0
        }
    }, {
        '$sort': {
            'x.year': 1,
            'x.month': 1,
            'x.date': 1,
            'x.hours': 1,
            'x.minutes': 1
        }
    }
]


print(pipeline[2]["$match"]["arg_file"]["$in"][0])