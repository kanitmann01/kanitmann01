# GitHub Stats Widgets

This document contains the markdown snippets for all dynamic stats widgets displayed on the profile README.

## Profile Views Counter

```markdown
<img src="https://komarev.com/ghpvc/?username=kanitmann01&label=Profile%20views&color=0e75b6&style=flat" alt="Profile views" />
```

## GitHub Stats Card

### Dark Theme

```markdown
<img src="https://github-readme-stats.vercel.app/api?username=kanitmann01&show_icons=true&theme=dark&hide_border=true" alt="GitHub Stats" align="center" />
```

### Light Theme

```markdown
<img src="https://github-readme-stats.vercel.app/api?username=kanitmann01&show_icons=true&theme=default&hide_border=true" alt="GitHub Stats" align="center" />
```

## Top Languages Card

### Dark Theme

```markdown
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=kanitmann01&layout=compact&theme=dark&hide_border=true" alt="Top Languages" align="center" />
```

### Light Theme

```markdown
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=kanitmann01&layout=compact&theme=default&hide_border=true" alt="Top Languages" align="center" />
```

## GitHub Streak Stats

### Dark Theme

```markdown
<img src="https://github-readme-streak-stats.herokuapp.com/?user=kanitmann01&theme=dark&hide_border=true" alt="GitHub Streak" align="center" />
```

### Light Theme

```markdown
<img src="https://github-readme-streak-stats.herokuapp.com/?user=kanitmann01&theme=default&hide_border=true" alt="GitHub Streak" align="center" />
```

## Contribution Snake Animation

```markdown
<img src="https://raw.githubusercontent.com/kanitmann01/kanitmann01/output/github-contribution-grid-snake.svg" alt="Contribution Snake" />
```

The snake SVG is generated automatically by the GitHub Actions workflow at `.github/workflows/snake.yml`.

## Theme-Aware Embedding

To support both light and dark GitHub themes, use the `#gh-dark-mode-only` and `#gh-light-mode-only` fragment identifiers:

```markdown
<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=kanitmann01&show_icons=true&theme=dark&hide_border=true#gh-dark-mode-only" alt="GitHub Stats (Dark)" />
  <img src="https://github-readme-stats.vercel.app/api?username=kanitmann01&show_icons=true&theme=default&hide_border=true#gh-light-mode-only" alt="GitHub Stats (Light)" />
</p>
```
