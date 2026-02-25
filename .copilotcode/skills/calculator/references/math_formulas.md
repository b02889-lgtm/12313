# Mathematical Formulas Reference

## Algebra

### Quadratic Formula
For equation ax² + bx + c = 0:
```
x = (-b ± √(b² - 4ac)) / (2a)
```

### Binomial Theorem
```
(a + b)ⁿ = Σ C(n,k) * aⁿ⁻ᵏ * bᵏ
where C(n,k) = n! / (k!(n-k)!)
```

### Logarithm Rules
- log(ab) = log(a) + log(b)
- log(a/b) = log(a) - log(b)
- log(aⁿ) = n·log(a)
- log_b(a) = log(a) / log(b)

## Calculus

### Derivatives

**Basic Rules:**
- d/dx(xⁿ) = n·xⁿ⁻¹
- d/dx(sin(x)) = cos(x)
- d/dx(cos(x)) = -sin(x)
- d/dx(eˣ) = eˣ
- d/dx(ln(x)) = 1/x

**Product Rule:**
```
d/dx[f(x)·g(x)] = f'(x)·g(x) + f(x)·g'(x)
```

**Quotient Rule:**
```
d/dx[f(x)/g(x)] = [f'(x)·g(x) - f(x)·g'(x)] / g(x)²
```

**Chain Rule:**
```
d/dx[f(g(x))] = f'(g(x))·g'(x)
```

### Integration

**Basic Integrals:**
- ∫ xⁿ dx = xⁿ⁺¹/(n+1) + C
- ∫ eˣ dx = eˣ + C
- ∫ 1/x dx = ln|x| + C
- ∫ sin(x) dx = -cos(x) + C
- ∫ cos(x) dx = sin(x) + C

**Integration by Parts:**
```
∫ u dv = uv - ∫ v du
```

## Trigonometry

### Pythagorean Identity
```
sin²(θ) + cos²(θ) = 1
```

### Angle Sum Formulas
- sin(α + β) = sin(α)cos(β) + cos(α)sin(β)
- cos(α + β) = cos(α)cos(β) - sin(α)sin(β)
- tan(α + β) = [tan(α) + tan(β)] / [1 - tan(α)tan(β)]

### Double Angle Formulas
- sin(2θ) = 2sin(θ)cos(θ)
- cos(2θ) = cos²(θ) - sin²(θ) = 2cos²(θ) - 1 = 1 - 2sin²(θ)
- tan(2θ) = 2tan(θ) / (1 - tan²(θ))

## Statistics

### Measures of Center
- **Mean**: μ = (Σxᵢ) / n
- **Median**: Middle value when sorted
- **Mode**: Most frequent value

### Measures of Spread
- **Variance**: σ² = Σ(xᵢ - μ)² / n
- **Standard Deviation**: σ = √(variance)
- **Range**: max - min

### Correlation
**Pearson Correlation Coefficient:**
```
r = Σ[(xᵢ - x̄)(yᵢ - ȳ)] / √[Σ(xᵢ - x̄)² · Σ(yᵢ - ȳ)²]
```

### Linear Regression
For y = mx + b:
```
m = Σ[(xᵢ - x̄)(yᵢ - ȳ)] / Σ(xᵢ - x̄)²
b = ȳ - mx̄
```

### Probability Distributions

**Normal Distribution:**
```
f(x) = (1/(σ√(2π))) · e^(-(x-μ)²/(2σ²))
```

**Binomial Distribution:**
```
P(X = k) = C(n,k) · pᵏ · (1-p)ⁿ⁻ᵏ
where C(n,k) = n!/(k!(n-k)!)
```

## Linear Algebra

### Matrix Operations

**Matrix Multiplication:**
If A is m×n and B is n×p, then C = AB is m×p where:
```
Cᵢⱼ = Σ(Aᵢₖ · Bₖⱼ)
```

**Determinant (2×2):**
```
det([a b]) = ad - bc
    [c d]
```

**Determinant (3×3):**
```
det([a b c]) = a(ei - fh) - b(di - fg) + c(dh - eg)
    [d e f]
    [g h i]
```

**Matrix Inverse (2×2):**
```
A⁻¹ = (1/det(A)) · [d  -b]
                    [-c  a]
where A = [a b]
          [c d]
```

### Vector Operations

**Dot Product:**
```
a · b = |a| |b| cos(θ) = a₁b₁ + a₂b₂ + a₃b₃
```

**Cross Product (3D):**
```
a × b = (a₂b₃ - a₃b₂)i + (a₃b₁ - a₁b₃)j + (a₁b₂ - a₂b₁)k
```

## Combinatorics

### Permutations
Number of ways to arrange n items taken k at a time:
```
P(n,k) = n! / (n-k)!
```

### Combinations
Number of ways to choose k items from n items:
```
C(n,k) = n! / (k!(n-k)!)
```

## Number Theory

### Greatest Common Divisor (GCD)
Euclidean Algorithm:
```
gcd(a, b) = gcd(b, a mod b)
gcd(a, 0) = a
```

### Least Common Multiple (LCM)
```
lcm(a, b) = |a × b| / gcd(a, b)
```

## Financial Mathematics

### Compound Interest
```
A = P(1 + r/n)^(nt)
where:
A = final amount
P = principal
r = annual rate
n = compounds per year
t = time in years
```

### Present Value
```
PV = FV / (1 + r)ⁿ
where:
PV = present value
FV = future value
r = rate per period
n = number of periods
```

### Annuity
```
PV = PMT × [(1 - (1 + r)^(-n)) / r]
where:
PMT = payment per period
r = rate per period
n = number of periods