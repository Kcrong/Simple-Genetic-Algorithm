"""
Author Kcrong
"""
from random import uniform


# According to PEP8, do not assign lambda
def rand(x, y): return int(uniform(x, y))


# 원하는 값
WE_WANT = [0, 0, 0, 0, 1, 1, 1, 1]


class Generation:
    cnt = 0

    def __new__(cls, *args, **kwargs):
        cls.cnt += 1

    def __init__(self, dna_list):
        self.generation_level = Generation.cnt
        self.generation = dna_list
        self.select_list = self.make_select_list()

    def __repr__(self):
        return "<Generation %d>" % self.generation_level

    def make_select_list(self):
        """
        dna fitness 만큼의 갯수를 가지는 dna 리스트
        dna1.fitness = 2,
        dna2.fitness = 3, then

        return [dna1, dna1, dna2, dna2, dna2]
        """

        tmp_list = list()

        for dna in self.generation:
            tmp_list += [dna for i in range(dna.fitness)]

        return tmp_list


class DNA:
    def __init__(self, gene_data=None):
        # 유전자 정보
        if gene_data is None:
            self.gene_data = [rand(0, 2) for i in range(len(WE_WANT))]
        else:
            self.gene_data = gene_data

    def __repr__(self):
        return "< Gene %s | %d >" % ("_".join(str(x) for x in self.gene_data), self.fitness)

    @property
    def fitness(self) -> int:
        """
        적합도 계산 함수
        :return: 0 ~ len(data) 사이의 적합도 값
        """
        score = 0

        for gene, want in zip(self.gene_data, WE_WANT):
            if gene == want:
                score += 1

        return score

    @staticmethod
    def make_child(parent1, parent2):
        """
        :param parent1: Parent Gene Object
        :param parent2: Parnet Gene Object
        :return: Child Gene Object
        """

        # 자식 유전자
        gene_data = list()

        # 두 부모를 튜플로 정의
        parents = (parent1, parent2)

        # 유전자 정보 길이
        gene_len = len(parent1.gene_data)

        # 각 교차 포인트를 정한다.
        # rand 함수의 반환이 float 형이므로, 소수점을 버리기 위해 int() 형변한을 해준다.
        switch_point = (rand(1, gene_len), rand(2, gene_len))

        # 처음 자식이 받는 유전자는 parent1
        # 다만 교차 포인트에 다다르면, 다른 parent 유전자 정보를 받아오기 시작한다. (parent = parent2)
        parent = parent1

        for i in range(gene_len):
            # 자식 유전자 정보는 부모 유전자에서 받아온다
            gene_data[i] = parent.gene_data[i]

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

        return DNA(gene_data)


if __name__ == '__main__':

    print(1)
