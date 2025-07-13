# Contributing to Educational Rummikub

We welcome contributions that make this codebase even better for learning! Here's how you can help.

## Our Goals

Remember, this project is designed to be:
- ✨ **Clear** - Easy to read and understand
- 📚 **Educational** - Great for learning Python
- 🎮 **Functional** - A working, enjoyable game
- 🚀 **Simple** - No unnecessary complexity

## Ways to Contribute

### 1. Report Issues
Found something confusing or broken? Let us know!
- Unclear documentation
- Bugs in the game
- Confusing code sections
- Missing explanations

### 2. Improve Documentation
Help make things clearer:
- Fix typos or grammar
- Add helpful examples
- Clarify confusing sections
- Add diagrams or visuals

### 3. Enhance the Code
Make the code better while keeping it simple:
- Fix bugs
- Improve error messages
- Add helpful comments
- Refactor unclear sections

### 4. Add Tests
Help ensure the game works correctly:
- Add missing test cases
- Test edge cases
- Improve test documentation

## Before You Start

### 1. Check Existing Issues
Someone might already be working on what you want to do.

### 2. Discuss Big Changes
For major changes, open an issue first to discuss your idea.

### 3. Keep It Simple
Remember: clarity over cleverness. Would a beginner understand your change?

## Making Changes

### 1. Get the Code
```bash
# Fork the repository first, then:
git clone https://github.com/your-username/educational-rummikub.git
cd educational-rummikub
```

### 2. Create a Branch
```bash
git checkout -b my-helpful-change
```

### 3. Make Your Changes
- Follow the existing code style
- Add comments for complex parts
- Update tests if needed
- Test your changes thoroughly

### 4. Test Everything
```bash
# Run the game
python main.py

# Run tests
python -m unittest discover tests/
```

### 5. Commit Your Changes
```bash
git add .
git commit -m "Clear description of what you changed"
```

## Submitting Changes

### 1. Push Your Branch
```bash
git push origin my-helpful-change
```

### 2. Create a Pull Request
- Go to GitHub
- Click "Create Pull Request"
- Describe your changes clearly
- Explain why they improve the project

### 3. Wait for Review
- Be patient - reviewers are volunteers
- Be open to feedback
- Make requested changes promptly

## Code Style Guidelines

### Python Style
```python
# Good: Clear and simple
def calculate_score(tiles):
    """Calculate the total value of tiles."""
    total = 0
    for tile in tiles:
        total += tile.get_value()
    return total

# Avoid: Too clever
def calculate_score(tiles):
    return sum(t.get_value() for t in tiles)
```

### Comments
```python
# Good: Explains why
# Jokers are worth 30 points when calculating penalties
if tile.is_joker():
    score += 30

# Avoid: Explains what (obvious from code)
# Add 30 to score
score += 30
```

### Naming
- Use descriptive names: `player_tiles` not `pt`
- Follow Python conventions: `snake_case` for functions
- Be consistent with existing code

## What Makes a Good Contribution?

### ✅ Good Contributions:
- Make the code clearer
- Fix actual problems
- Add helpful documentation
- Improve error messages
- Add missing tests

### ❌ Avoid:
- Adding unnecessary complexity
- Using advanced Python features just because you can
- Changing things that already work well
- Adding dependencies

## Documentation Contributions

When improving documentation:
1. **Use simple language** - Avoid jargon
2. **Add examples** - Show, don't just tell
3. **Think like a beginner** - What would confuse someone new?
4. **Test your instructions** - Do they actually work?

## Getting Help

If you're stuck:
1. Check the [documentation](index.md)
2. Look at existing code for examples
3. Ask in your pull request
4. Open an issue with your question

## Recognition

All contributors will be acknowledged in the project. Your help makes this a better learning resource for everyone!

## Code of Conduct

- Be respectful and welcoming
- Help others learn
- Accept constructive feedback gracefully
- Focus on what's best for learners

Remember: We're all here to learn and help others learn. Every contribution, no matter how small, is valuable!

---

Thank you for helping make Educational Rummikub better! 🎉