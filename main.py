"""
Author Kcrong
"""
from random import uniform

from matplotlib.pyplot import plot, show, xlim, ylim, xlabel, ylabel
from numpy import mean


# According to PEP8, do not assign lambda
def rand(x, y): return int(uniform(x, y))


# 원하는 값
WE_WANT = [0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0]

# 우월 유전자 보존 갯수
GOOD_DNA_CNT = 5

# 돌연변이 확률은 fitness 와 반비례 한다.
# fitness 가 높을 수록, 돌연변이 확률이 적어진다.
MUTATION_PROBABILITY = 10


class Generation:
    cnt = 0

    def __init__(self, dna_list):
        Generation.cnt += 1
        self.generation_level = Generation.cnt
        self.DNA_list = dna_list
        self.select_list = self.make_select_list()

    def __repr__(self):
        return "<Generation level %d>" % self.generation_level

    def make_select_list(self):
        """
        dna fitness 만큼의 갯수를 가지는 dna 리스트
        dna1.fitness = 2,
        dna2.fitness = 3, then

        return [dna1, dna1, dna2, dna2, dna2]
        """

        tmp_list = list()

        for dna in self.DNA_list:
            tmp_list += [dna for i in range(dna.fitness)]

        return tmp_list

    def make_child(self):
        """
        :return: Child Gene Object
        """

        if rand(0, self.fitness * MUTATION_PROBABILITY) == 0:
            return DNA([rand(min(WE_WANT), max(WE_WANT)) for i in range(len(WE_WANT))])

        # 부모를 select_list 를 이용해 정함.
        # 부모로 선출될 확률은 fitness 과 비례한다.
        parents = tuple(self.select_list[rand(0, len(self.select_list))] for i in range(2))

        # 자식 유전자
        gene_data = list()

        # 유전자 정보 길이
        gene_len = len(parents[0].gene_data)

        # 각 교차 포인트를 정한다.
        # rand 함수의 반환이 float 형이므로, 소수점을 버리기 위해 int() 형변한을 해준다.
        switch_point = (rand(1, gene_len // 2), rand(gene_len // 2, gene_len))

        # 처음 자식이 받는 유전자는 parent1
        # 다만 교차 포인트에 다다르면, 다른 parent 유전자 정보를 받아오기 시작한다. (parent = parent2)
        parent = parents[0]

        for i in range(gene_len):
            # 자식 유전자 정보는 부모 유전자에서 받아온다
            gene_data.append(parent.gene_data[i])

            if i in switch_point:
                # 유전자를 받아오는 부모 변경
                try:
                    parent = parents[parents.index(parent) + 1]
                except IndexError:
                    parent = parents[0]

                """
                a = parents.index(parent) --> 현재 부모의 index 값
                parents[a+1] --> 부모 리스트에서, 현재 부모 인덱스값보다 +1 된 값 가져옴
                IndexError --> 만약 1이 넘어가면
                parent = parents[0] 다시 0으로 돌아옴
                """

        # return DNA(gene_data)
        dna = DNA(gene_data)
        return dna

    def evolution(self):
        print("Start Evolution Generation level %d" % Generation.cnt)

        dna_list = [self.best for i in range(GOOD_DNA_CNT)]
        dna_list += [self.make_child() for i in range(len(self.DNA_list) - len(dna_list))]

        return Generation(dna_list)

    @property
    def fitness(self):
        # 세대 객체의 평균 적합도
        return mean([dna.fitness for dna in self.DNA_list])

    @property
    def best(self):
        return sorted(self.DNA_list, key=lambda x: x.fitness, reverse=True)[0]


class DNA:
    def __init__(self, gene_data=None):
        # 유전자 정보
        if gene_data is None:
            self.gene_data = [rand(min(WE_WANT), max(WE_WANT) + 1) for i in range(len(WE_WANT))]
        else:
            self.gene_data = gene_data

    def __repr__(self):
        return "< Gene %s | %d >" % ("_".join(str(x) for x in self.gene_data), self.fitness)

    @staticmethod
    def max_fitness():
        if max(WE_WANT) < 2:
            return len(WE_WANT) * max(WE_WANT)
        else:
            return len(WE_WANT) * (max(WE_WANT) // 2)

    @property
    def fitness(self) -> int:
        """
        적합도 계산 함수
        :return: 적합도 값
        """

        score = DNA.max_fitness()

        for gene, want in zip(self.gene_data, WE_WANT):
            if gene != want:
                score -= abs(gene - want)

        return score


def visualization(generations):
    fitness_list = [generation.fitness for generation in generations]

    # 최대 적합도를 그래프에 나타냄
    max_fitness = DNA.max_fitness()
    plot([max_fitness for i in range(len(generations))])

    xlim([0, len(generations)])

    # 축의 lim 값을 데이터 보다 높게 잡아줌으로써, 그래프의 가독성을 높임
    ylim([int(min(fitness_list)), (DNA.max_fitness() * 1.2)])

    xlabel('Generation')
    ylabel('Fitness Score')

    # 각 세대의 (평균) 적합도를 이용해 그래프에 나타냄
    plot([generation.fitness for generation in generations])

    show()


if __name__ == '__main__':
    Generations = list()

    # 첫 세대 (조상 세대)
    Generations.append(Generation([DNA() for i in range(100)]))

    i = 0
    while True:
        try:
            next_generation = Generations[i].evolution()
            Generations.append(next_generation)
            print("Fitness: %d" % next_generation.fitness)
            print("Best DNA: %s" % next_generation.best)

            # 적합도가 최대일 경우, 반복문 종료
            if next_generation.fitness >= DNA.max_fitness():
                break
            i += 1
        except KeyboardInterrupt:
            break

    print("Last Generation's Best DNA: %s" % Generations[-1].best)

    visualization(Generations)
