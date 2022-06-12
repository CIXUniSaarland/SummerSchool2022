from bisect import bisect


class Grid:
    def __init__(self, domain):
        self.domain = domain
        self.values = {d: 1.0 / len(domain) for d in domain}

    @classmethod
    def uniform(cls, start, stop, n):
        """Create a uniform grid from start to stop, with n steps"""
        return Grid(np.linspace(start, stop, n))

    def delta(self, delta):
        """Create a a grid with all probability on one outcome"""
        self.values = {d: 0 for d in self.domain}
        g[delta] = 1.0

    def norm(self, mean, std):
        """Create a a grid with approximately Gaussian distribuion"""
        self.values = {d: ss.norm(mean, std).pdf(d) for d in self.domain}
        self.normalise()

    def at(self, v):
        """Return the index of the grid element with the given value."""
        assert np.min(self.domain) <= v <= np.max(self.domain)
        return bisect(self.domain, v)

    def __getitem__(self, v):
        """Return the value associated with the bin nearest v"""
        return self.values[self.domain[self.at(v)]]

    def __setitem__(self, v, p):
        """Set the value associated with the bin nearest v"""
        self.values[self.domain[self.at(v)]] = p

    def integrate(self, start=None, stop=None):
        """Return the sum of probabilities inside a range"""
        if start is None:
            start = self.domain[0]

        if stop is None:
            stop = self.domain[-1]
        return sum(
            [self.values[d] for d in self.domain[self.at(start) : self.at(stop)]]
        )

    def normalise(self):
        """Normalise a distribution"""
        total = self.integrate()
        self.values = {d: v / total for d, v in self.values.items()}

    def __str__(self):
        """Print out the grid descriptor"""
        chars = " ░▒▓█"
        bars = "▁▂▃▄▅▆▇█"

        def map_char(p):
            if p < 1e-9:
                return " "
            if p > (1 - 1e-9):
                return "█"
            q = 0.25 * np.log10(p / (1 - p))
            q = int(np.clip(0, q + len(bars) / 2, len(bars) - 1))
            return bars[q]

        return f"{self.domain[0]:.1f} {' '.join(map_char(p) for p in self.values.values())} {self.domain[-1]:.1f}"

    def __repr__(self):
        return str(self)


g = Grid.uniform(0, 1, 10)
g.delta(0.5)
g
g
