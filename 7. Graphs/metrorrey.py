from graph import Graph


if __name__ == '__main__':
    metrorrey: Graph[str] = Graph(['Talleres',
                                   'San Bernabé',
                                   ])
    metrorrey.add_edge_by_vertices('Talleres', 'San Bernabé')
    print(metrorrey)
