# Nepali Language

नेपाली भाषामा programming गर्न बनाइएको सरल programming language।

**Version:** `0.1.0`

---

## मुख्य विशेषताहरू

Nepali Language मा अहिले यी features उपलब्ध छन्:

- नेपाली keywords
- Variables
- पूर्णाङ्क
- दशमलव
- पाठ
- सत्य / गलत
- सूची
- नक्सा
- Arithmetic operators
- Comparison operators
- Boolean operators
- Modulo `%`
- Power `^`
- यदि
- नत्र
- अन्यथा
- जब loop
- हरेक loop
- रोक
- जारी
- Functions
- Return
- Import system
- Standard Library
- File read/write
- JSON
- Runtime error location
- Lexer error location
- Parser error location
- REPL
- Formatter
- Automated tests
- Project config (`nep.json`)

---

# Hello World

```nep
देखाऊ("नमस्ते संसार")
```

चलाउन:

```powershell
nep run .\examples\main.nep
```

---

# Variables

## पूर्णाङ्क

```nep
पूर्णाङ्क उमेर = 25
देखाऊ(उमेर)
```

## दशमलव

```nep
दशमलव मूल्य = 10.5
देखाऊ(मूल्य)
```

## पाठ

```nep
पाठ नाम = "अमृत"
देखाऊ(नाम)
```

## सत्य / गलत

```nep
सत्य सक्रिय = सही
देखाऊ(सक्रिय)
```

---

# Arithmetic

```nep
पूर्णाङ्क क = 10
पूर्णाङ्क ख = 20

देखाऊ(क + ख)
देखाऊ(ख - क)
देखाऊ(क * ख)
देखाऊ(ख / क)
```

---

# Modulo

Modulo का लागि `%` प्रयोग गर्न सकिन्छ।

```nep
देखाऊ(10 % 3)
```

Output:

```text
1
```

जोर/बिजोर जाँच्न पनि `%` प्रयोग गर्न सकिन्छ:

```nep
यदि (10 % 2 == 0) {
    देखाऊ("जोर")
} अन्यथा {
    देखाऊ("बिजोर")
}
```

---

# Power

Power/Exponent का लागि `^` प्रयोग गर्न सकिन्छ।

```nep
देखाऊ(2 ^ 3)
```

Output:

```text
8
```

Power operator right-associative छ।

```nep
देखाऊ(2 ^ 3 ^ 2)
```

यसको अर्थ:

```text
2 ^ (3 ^ 2)
```

त्यसैले output:

```text
512
```

---

# Comparison

```nep
देखाऊ(10 > 5)
देखाऊ(10 < 20)
देखाऊ(10 >= 10)
देखाऊ(5 <= 10)
देखाऊ(10 == 10)
देखाऊ(10 != 5)
```

---

# Boolean Operators

```nep
सत्य क = सही
सत्य ख = गलत

देखाऊ(क र ख)
देखाऊ(क वा ख)
देखाऊ(होइन ख)
```

---

# यदि / अन्यथा

```nep
पूर्णाङ्क उमेर = 20

यदि (उमेर >= 18) {
    देखाऊ("वयस्क")
} अन्यथा {
    देखाऊ("नाबालक")
}
```

पुरानो `नत्र` syntax पनि प्रयोग गर्न सकिन्छ:

```nep
पूर्णाङ्क उमेर = 15

यदि (उमेर >= 18) {
    देखाऊ("वयस्क")
} नत्र {
    देखाऊ("नाबालक")
}
```

---

# जब Loop

```nep
पूर्णाङ्क संख्या = 0

जब (संख्या < 5) {
    देखाऊ(संख्या)
    संख्या = संख्या + 1
}
```

---

# हरेक Loop

```nep
सूची फलहरू = [
    "स्याउ",
    "केरा",
    "सुन्तला"
]

हरेक फल मा फलहरू {
    देखाऊ(फल)
}
```

---

# रोक र जारी

Loop भित्र:

```text
रोक
```

ले loop रोक्न प्रयोग हुन्छ।

```text
जारी
```

ले अर्को iteration मा जान प्रयोग हुन्छ।

---

# सूची

```nep
सूची फलहरू = [
    "स्याउ",
    "केरा"
]

देखाऊ(फलहरू)
देखाऊ(फलहरू[0])
```

---

# नक्सा

```nep
नक्सा प्रयोगकर्ता = {
    "नाम": "अमृत",
    "उमेर": 25
}

देखाऊ(प्रयोगकर्ता["नाम"])
देखाऊ(प्रयोगकर्ता["उमेर"])
```

नयाँ value थप्न:

```nep
प्रयोगकर्ता["देश"] = "नेपाल"

देखाऊ(प्रयोगकर्ता)
```

---

# Functions

```nep
काम जोड(
    पूर्णाङ्क क,
    पूर्णाङ्क ख
) -> पूर्णाङ्क {
    फर्काऊ क + ख
}

पूर्णाङ्क नतिजा = जोड(10, 20)

देखाऊ(नतिजा)
```

Output:

```text
30
```

---

# Import

Local `.nep` file import गर्न:

```nep
प्रयोग "गणित.nep"
```

Standard Library module छोटो नामबाट import गर्न:

```nep
प्रयोग "गणित"
```

---

# Standard Library

अहिले उपलब्ध Standard Library modules:

```text
गणित
संख्या
पाठ
सूची
नक्सा
तर्क
```

---

# गणित Standard Library

Import:

```nep
प्रयोग "गणित"
```

उदाहरण:

```nep
प्रयोग "गणित"

देखाऊ(जोड(10, 20))
देखाऊ(घटाऊ(20, 10))
देखाऊ(गुणा(5, 5))
देखाऊ(भाग(100, 4))
देखाऊ(वर्ग(5))
देखाऊ(घन(3))
देखाऊ(घात(2, 3))
```

उपलब्ध functions:

```text
जोड()
घटाऊ()
गुणा()
भाग()
वर्ग()
घन()
घात()
```

---

# संख्या Standard Library

Import:

```nep
प्रयोग "संख्या"
```

उदाहरण:

```nep
प्रयोग "संख्या"

देखाऊ(धनात्मक(10))
देखाऊ(ऋणात्मक(-10))
देखाऊ(शून्यहो(0))

देखाऊ(ठूलो(10, 20))
देखाऊ(सानो(10, 20))
देखाऊ(निरपेक्ष(-50))

देखाऊ(जोर(10))
देखाऊ(बिजोर(7))
```

उपलब्ध functions:

```text
धनात्मक()
ऋणात्मक()
शून्यहो()
ठूलो()
सानो()
निरपेक्ष()
जोर()
बिजोर()
```

---

# पाठ Standard Library

Import:

```nep
प्रयोग "पाठ"
```

उदाहरण:

```nep
प्रयोग "पाठ"

पाठ नाम = "अमृत"

देखाऊ(खालीछ(नाम))
देखाऊ(खालीछ(""))
देखाऊ(खालीछैन(नाम))
देखाऊ(बराबर(नाम, "अमृत"))
देखाऊ(फरक(नाम, "राम"))
देखाऊ(लामोछ(नाम, 3))
देखाऊ(छोटोछ(नाम, 10))
```

---

# सूची Standard Library

Import:

```nep
प्रयोग "सूची"
```

उदाहरण:

```nep
प्रयोग "सूची"

सूची फलहरू = [
    "स्याउ",
    "केरा"
]

देखाऊ(सूचीलम्बाइ(फलहरू))
देखाऊ(खालीसूची(फलहरू))
देखाऊ(सूचीछैनखाली(फलहरू))
देखाऊ(सूचीमाछ(फलहरू, "स्याउ"))

सूचीथप(
    फलहरू,
    "सुन्तला"
)

देखाऊ(फलहरू)

सूचीहटाऊ(
    फलहरू,
    "केरा"
)

देखाऊ(फलहरू)
```

---

# नक्सा Standard Library

Import:

```nep
प्रयोग "नक्सा"
```

उदाहरण:

```nep
प्रयोग "नक्सा"

नक्सा प्रयोगकर्ता = {
    "नाम": "अमृत",
    "उमेर": 25
}

देखाऊ(नक्सालम्बाइ(प्रयोगकर्ता))
देखाऊ(खालीनक्सा(प्रयोगकर्ता))
देखाऊ(नक्साछैनखाली(प्रयोगकर्ता))
देखाऊ(keyछ(प्रयोगकर्ता, "नाम"))
```

---

# तर्क Standard Library

Import:

```nep
प्रयोग "तर्क"
```

उदाहरण:

```nep
प्रयोग "तर्क"

देखाऊ(उल्टो(सही))
देखाऊ(दुवै(सही, गलत))
देखाऊ(कुनैएक(सही, गलत))
देखाऊ(दुवैसही(सही, सही))
देखाऊ(दुवैगलत(गलत, गलत))
देखाऊ(एउटामात्र(सही, गलत))
```

---

# Built-in Functions

## लम्बाइ

```nep
देखाऊ(लम्बाइ("नेपाल"))
```

सूचीमा पनि प्रयोग गर्न सकिन्छ:

```nep
सूची अंकहरू = [1, 2, 3]

देखाऊ(लम्बाइ(अंकहरू))
```

---

## पूर्णाङ्कमा

```nep
पूर्णाङ्क संख्या = पूर्णाङ्कमा("25")

देखाऊ(संख्या)
```

---

## दशमलवमा

```nep
दशमलव संख्या = दशमलवमा("10.5")

देखाऊ(संख्या)
```

---

## पाठमा

```nep
पाठ मान = पाठमा(100)

देखाऊ(मान)
```

---

# JSON

JSON बनाउन:

```nep
पाठ json = JSONबनाऊ(
    {
        "नाम": "अमृत",
        "उमेर": 25
    }
)

देखाऊ(json)
```

JSON पढ्न:

```nep
नक्सा data = JSONपढ(json)

देखाऊ(data)
```

---

# File I/O

File लेख्न:

```nep
फाइललेख(
    "hello.txt",
    "नमस्ते नेपाल"
)
```

File पढ्न:

```nep
पाठ content = फाइलपढ(
    "hello.txt"
)

देखाऊ(content)
```

File छ कि छैन जाँच्न:

```nep
देखाऊ(
    फाइलछकि(
        "hello.txt"
    )
)
```

---

# CLI

## Help

```powershell
nep help
```

## Version

```powershell
nep version
```

## Program चलाउन

```powershell
nep run program.nep
```

उदाहरण:

```powershell
nep run .\examples\main.nep
```

## Project main file चलाउन

यदि `nep.json` मा main file सेट गरिएको छ भने:

```powershell
nep run
```

मात्र लेखेर project चलाउन सकिन्छ।

## Syntax Check

```powershell
nep check program.nep
```

## Formatter

```powershell
nep fmt program.nep
```

## Tests

```powershell
nep test
```

## REPL

```powershell
nep repl
```

## नयाँ Project

```powershell
nep new MyProject
```

## Current Folder Initialize

```powershell
nep init
```

---

# nep.json

Project configuration example:

```json
{
  "name": "Nepali-Language",
  "version": "0.1.0",
  "main": "examples/main.nep"
}
```

यहाँ:

```json
"main": "examples/main.nep"
```

ले project को मुख्य program कुन हो भनेर बताउँछ।

त्यसपछि:

```powershell
nep run
```

ले `examples/main.nep` automatically चलाउँछ।

---

# Error Reporting

Nepali Language ले error हुँदा file, line र column जानकारी देखाउन सक्छ।

उदाहरण:

```text
त्रुटि: Variable भेटिएन: नाम
फाइल: test.nep | लाइन: 3 | स्तम्भ: 8
```

Imported `.nep` file मा error भएमा पनि imported file को location देखाइन्छ।

---

# Testing

सबै automated tests चलाउन:

```powershell
nep test
```

Development को क्रममा language का मुख्य features automated tests बाट जाँचिन्छन्।

अहिलेसम्म tests मा यस्ता features समावेश छन्:

- Variables
- Arithmetic
- Boolean
- Lists
- List indexing
- Maps
- Functions
- While loops
- For-each loops
- Import
- Runtime error location
- `नत्र`
- `अन्यथा`
- Modulo `%`
- Power `^`
- Number Standard Library
- Math Standard Library
- Error handling

---

# Project Structure

```text
Nepali-Language
│
├── nep.py
├── nep.bat
├── nep.json
├── README.md
│
├── src
│   ├── lexer.py
│   ├── parser.py
│   ├── interpreter.py
│   └── errors.py
│
├── stdlib
│   ├── गणित.nep
│   ├── संख्या.nep
│   ├── पाठ.nep
│   ├── सूची.nep
│   ├── नक्सा.nep
│   └── तर्क.nep
│
├── examples
│   └── main.nep
│
└── tests
    ├── test_language.py
    └── test_errors.py
```

---

# Version

Current development version:

```text
0.1.0
```

---

# उद्देश्य

Nepali Language को उद्देश्य नेपाली भाषाबाट programming सिक्न र program लेख्न सरल वातावरण उपलब्ध गराउनु हो।

यस project मार्फत नेपाली keywords प्रयोग गरेर programming का आधारभूत concepts सिक्न र program बनाउन सकिन्छ।