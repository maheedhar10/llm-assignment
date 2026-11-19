# Task 3 - same 10 prompts, two quantisation levels

## Prompt 1 (fact)

**Prompt:** What is the capital of Australia? Answer in one word.

**Expected:** Canberra

**qwen2.5:1.5b-instruct-fp16:**

```
Canberra
```

**qwen2.5:1.5b-instruct-q4_K_M:**

```
Canberra
```

**My observation:** _write here_

---

## Prompt 2 (math word problem)

**Prompt:** A shop sells pens at 3 for 45 rupees. How much do 7 pens cost? Show your working briefly.

**Expected:** 105 rupees

**qwen2.5:1.5b-instruct-fp16:**

```
To find the cost of 7 pens, we first need to determine the cost of one pen. We know that 3 pens cost 45 rupees. Therefore, the cost of one pen is:

\[ \text{Cost of one pen} = \frac{45 \text{ rupees}}{3 \text{ pens}} = 15 \text{ rupees per pen} \]

Now that we know the cost of one pen, we can calculate the cost of 7 pens:

\[ \text{Cost of 7 pens} = 7 \text{ pens} \times 15 \text{ rupees per pen} = 105 \text{ rupees} \]

So, 7 pens cost 105 rupees.
```

**qwen2.5:1.5b-instruct-q4_K_M:**

```
To find out how much 7 pens cost, we first need to determine the cost of one pen. Since 3 pens cost 45 rupees, we can calculate the cost of one pen by dividing 45 rupees by 3.

\[ \text{Cost of one pen} = \frac{45 \text{ rupees}}{3} = 15 \text{ rupees} \]

Now that we know one pen costs 15 rupees, we can find the cost of 7 pens by multiplying the cost of one pen by 7.

\[ \text{Cost of 7 pens} = 15 \text{ rupees/pen} \times 7 \text{ pens} = 105 \text{ rupees} \]

So, 7 pens cost 105 rupees.
```

**My observation:** _write here_

---

## Prompt 3 (arithmetic)

**Prompt:** What is 17 multiplied by 24? Give only the number.

**Expected:** 408

**qwen2.5:1.5b-instruct-fp16:**

```
408
```

**qwen2.5:1.5b-instruct-q4_K_M:**

```
408
```

**My observation:** _write here_

---

## Prompt 4 (code)

**Prompt:** Write a Python function is_palindrome(s) that returns True if s is a palindrome, ignoring case and spaces. Code only.

**Expected:** correct, runnable function

**qwen2.5:1.5b-instruct-fp16:**

```
```python
def is_palindrome(s):
    """
    Check if the given string is a palindrome, ignoring case and spaces.
    
    Args:
    s (str): The string to check.
    
    Returns:
    bool: True if s is a palindrome, False otherwise.
    """
    # Remove spaces and convert to lowercase
    cleaned_s = ''.join(c for c in s if c.isalnum()).lower()
    # Check if the cleaned string is equal to its reverse
    return cleaned_s == cleaned_s[::-1]
```
```

**qwen2.5:1.5b-instruct-q4_K_M:**

```
```python
def is_palindrome(s):
    """
    Check if the given string is a palindrome, ignoring case and spaces.
    
    Parameters:
    s (str): The string to check.
    
    Returns:
    bool: True if s is a palindrome, False otherwise.
    """
    # Remove spaces and convert to lowercase
    cleaned_s = ''.join(filter(str.isalnum, s)).lower()
    
    # Check if the cleaned string is equal to its reverse
    return cleaned_s == cleaned_s[::-1]
```
```

**My observation:** _write here_

---

## Prompt 5 (strict JSON)

**Prompt:** Convert to JSON with keys name, age, city: 'Priya is 28 and lives in Pune.' Output only the JSON.

**Expected:** {"name": "Priya", "age": 28, "city": "Pune"}

**qwen2.5:1.5b-instruct-fp16:**

```
```json
{
  "name": "Priya",
  "age": 28,
  "city": "Pune"
}
```
```

**qwen2.5:1.5b-instruct-q4_K_M:**

```
```json
{
  "name": "Priya",
  "age": 28,
  "city": "Pune"
}
```
```

**My observation:** _write here_

---

## Prompt 6 (summarisation)

**Prompt:** Summarise in exactly two sentences: The city council approved a plan to convert three downtown parking lots into public parks. Supporters say the parks will reduce heat and give residents more green space, while some shop owners worry that fewer parking spaces will hurt their business. Construction is expected to begin next spring and finish within eighteen months.

**Expected:** 2 accurate sentences

**qwen2.5:1.5b-instruct-fp16:**

```
The city council approved a plan to convert three downtown parking lots into public parks, which supporters say will reduce heat and provide more green space for residents, while some shop owners worry that fewer parking spaces will hurt their business. Construction is expected to begin next spring and finish within eighteen months.
```

**qwen2.5:1.5b-instruct-q4_K_M:**

```
The city council approved a plan to convert three downtown parking lots into public parks, which supporters say will reduce heat and provide more green space for residents, while some shop owners worry that fewer parking spaces will hurt their business. Construction is expected to begin next spring and finish within eighteen months.
```

**My observation:** _write here_

---

## Prompt 7 (translation)

**Prompt:** Translate into French: 'The meeting has been moved to Thursday afternoon.'

**Expected:** La réunion a été déplacée à jeudi après-midi.

**qwen2.5:1.5b-instruct-fp16:**

```
La réunion a été transférée au après-midi de jeudi.
```

**qwen2.5:1.5b-instruct-q4_K_M:**

```
La réunion a été transférée au après-midi de jeudi.
```

**My observation:** _write here_

---

## Prompt 8 (format following)

**Prompt:** List exactly three advantages of solar energy as a numbered list. Nothing else.

**Expected:** exactly 3 numbered items

**qwen2.5:1.5b-instruct-fp16:**

```
1. **Renewable Resource**: Solar energy is a renewable resource, meaning it is inexhaustible and will never run out, unlike fossil fuels.
2. **Environmental Benefits**: Solar energy production has a minimal environmental impact compared to traditional energy sources, as it does not produce greenhouse gases or air pollutants.
3. **Cost-Effective**: The cost of solar energy technology has been decreasing over time, making it increasingly competitive with traditional energy sources in terms of cost.
```

**qwen2.5:1.5b-instruct-q4_K_M:**

```
1. Renewable resource: Solar energy is a naturally replenishing resource that will never run out.
2. Environmentally friendly: It produces no greenhouse gases or pollutants, making it a clean energy source.
3. Cost-effective: While initial installation costs can be high, the long-term savings on fuel and maintenance make solar energy a cost-effective option in the long run.
```

**My observation:** _write here_

---

## Prompt 9 (logic)

**Prompt:** If all bloops are razzies and all razzies are lazzies, are all bloops definitely lazzies? Answer yes or no, then explain in one sentence.

**Expected:** Yes

**qwen2.5:1.5b-instruct-fp16:**

```
Yes, all bloops are definitely lazzies because if all bloops are razzies and all razzies are lazzies, then the set of bloops is a subset of the set of lazzies.
```

**qwen2.5:1.5b-instruct-q4_K_M:**

```
Yes, all bloops are definitely lazzies. This is because if all bloops are razzies and all razzies are lazzies, then every bloop must also be a lazzie.
```

**My observation:** _write here_

---

## Prompt 10 (explanation)

**Prompt:** Explain what a hash table is to a 10-year-old in under 60 words.

**Expected:** simple, correct, < 60 words

**qwen2.5:1.5b-instruct-fp16:**

```
A hash table is like a special kind of toy box where you can quickly find your favorite toy. Imagine you have a bunch of toys, and each toy has a name tag. The toy box has a special rule to find the toy you want. If you know the name tag, you can quickly find the toy inside. This is similar to how a hash table works, but instead of toys and name tags, it uses numbers and keys to find information quickly.
```

**qwen2.5:1.5b-instruct-q4_K_M:**

```
A hash table is like a special kind of toy box where you can quickly find your favorite toy. Instead of looking through all the toys one by one, you can quickly find the toy you want by using a magic number (called a hash) that tells you exactly where to look. This makes it super fast to find things, just like how you can find your favorite toy in the toy box much faster than looking through all the other toys.
```

**My observation:** _write here_

---

