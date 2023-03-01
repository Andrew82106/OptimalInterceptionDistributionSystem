# -*- coding:utf-8 -*-
N = 2000005
c = [0] * N
a = [0] * N
ans = 0


class SAM:
    def __init__(self):
        self.s = ['']  # s从1开始存储
        self.n = 0
        self.last = 1
        self.cnt = 1
        self.ch = [[0] * 26 for _ in range(N << 1)]
        self.fa = [0] * (N << 1)
        self.l = [0] * (N << 1)
        self.size = [0] * (N << 1)

    def ins(self, c_: int) -> None:
        p = self.last
        np = self.last = self.cnt = self.cnt + 1
        self.l[np] = self.l[p] + 1
        while p and not self.ch[p][c_]:
            self.ch[p][c_] = np
            p = self.fa[p]
        if not p:
            self.fa[np] = 1
        else:
            q = self.ch[p][c_]
            if self.l[q] == self.l[p] + 1:
                self.fa[np] = q
            else:
                nq = self.cnt = self.cnt + 1
                self.l[nq] = self.l[p] + 1
                self.ch[nq] = self.ch[q][:]
                self.fa[nq] = self.fa[q]
                self.fa[q] = self.fa[np] = nq
                while p and self.ch[p][c_] == q:
                    self.ch[p][c_] = nq
                    p = self.fa[p]
        self.size[np] = 1

    def build(self, s_: str) -> None:
        self.s.extend(s_)
        self.n = len(self.s) - 1
        for i in range(1, self.n + 1):
            self.ins(ord(self.s[i]) - ord('a'))

    def calc(self) -> None:
        global ans
        for i in range(1, self.cnt + 1):
            c[self.l[i]] += 1
        for i in range(1, self.cnt + 1):
            c[i] += c[i - 1]
        for i in range(1, self.cnt + 1):
            a[c[self.l[i]]] = i
            c[self.l[i]] -= 1
        for i in range(self.cnt, 0, -1):
            p = a[i]
            self.size[self.fa[p]] += self.size[p]
            if self.size[p] > 1:
                ans = max(ans, self.size[p] * self.l[p])
        print(ans)


sam = SAM()
# s = input()
s = "babaabbbbbbabbaabaaaaabbbaabaabaabbabaaabababaaabbbbabbbaaabbbabbaababbbabbaabaaaaabbbaabaabaabbabbaabaaabbbbabbbaaabbbaababbbbbbaaababbbbabbaabaaaaabbbaabaabaabbabbababaabaaabbbbabbbaaabbbabbbaaaababaabbbbabbaabaaaaabbbaabaabaabbabbababaaabbbbabbbaaabbbaababbbabbaabaaaaabbbaabaabaabbababbabaaabbbbabbbaaabbbabaabaaaabbbbbabbaabaaaaabbbaabaabaabbabababaabaaabbbbabbbaaabbbbbaaabbbabbabbaabbbabbaabaaaaabbbaabaabaabbabbabbaaabbbbabbbaaabbbabbaaabbababbbabbaabaaaaabbbaabaabaabbabababbaaabbbbabbbaaabbbbaabbabaaabbbabbaabaaaaabbbaabaabaabbabaabaaabbbbabbbaaabbbbabbaabaaabbbabbaabaaaaabbbaabaabaabbabababbabbbbaaabbbbabbbaaabbbbbbbabbaaabbbabbaabaaaaabbbaabaabaabbabbbbaaabbbbabbbaaabbbabaabbabbbabbaabaaaaabbbaabaabaabbabbbbaabbababaaabbbbabbbaaabbbabbabaabbbabbaabaaaaabbbaabaabaabbabaabbbaaabbbbabbbaaabbbaaabbaababbbbbabbaabaaaaabbbaabaabaabbabaaabbaaabbbbabbbaaabbbbaaaababaabbbabbaabaaaaabbbaabaabaabbabbbaaabbbbabbbaaabbbaabbbbabbaabaaaaabbbaabaabaabbabbbabbbaaabbbbabbbaaabbbbabababbaabaaababa"
sam.build(s)
sam.calc()
