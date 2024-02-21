# ddg
Efforts to revive my 44-year-old SIMULA'67 project dealing with disjunctive graphs using Python now

Start date: 2024-02-21
Owner: FeJozsi from Budapest, Hungary
E-mail: jfeher@fjm.hu

2024-02-21 13:59:52: Theoretical background
    Directed disjunctive graphs can be conceptualized as collections of operations and machines,
    mirroring our intuitive understanding of these concepts.

    Each operation has a designated execution time and is assigned
    to a specific machine for execution.
    The workflow on machines is independent of the operations and their order,
    but each machine can handle only one operation at a time.
    In general, our task is to determine the sequence in which operations are executed
    on the machines. However, we must adhere to specific technological dependencies between
    operations, which are established at the outset.

    It is evident that technological dependencies cannot form a cycle between operations,
    as these relations dictate that one operation must precede the other in the sequence.

    Therefore, our objective is to find an order of operations on all machines that
    satisfies the requirements and minimizes the total execution time. Forty-four years ago,
    when I obtained my Master's degree in Mathematics, this task posed a significant
    challenge for the computers of that era. However, nowadays, it can still be
    challenging depending on the specific circumstances.

    We rewrote the old SIMULA'67 code in Python. The execution time improved significantly,
    among others, due to the increased speed of computers by at least five orders of magnitude.
    However, our task is extremely complex. I have developed a random "directed disjunctive
    graph" task generator (which will be added to the repository soon). With this tool,
    for example, I managed to create a very resource-intensive task consisting of
    one hundred operations and four machines – despite the fact that we exclude the
    "hopeless" branches of the solution tree to be traversed with sufficiently
    well-founded lower bound estimates. The thesis revolved around this topic.

    When we modify specific technological dependencies between tasks,
    it can greatly affect the resources needed to find the optimum solution.
