### Boilerplate dos Katas e Suíte de Testes Automatizados (`katas/kata-00-teste-string-transformer/`)

**Objetivo:** Estruturar os exercícios (katas) de forma isolada, definindo as funções/classes que devem ser implementadas e os **testes unitários automatizados** para validação imediata durante a Sprint 2.

#### Como funciona (Passo a Passo)

1. **Seleção e Padronização dos Katas:**
* Selecionar de 4 a 6 katas de nível equivalente em JavaScript (ex.: *FizzBuzz*, *Roman Numerals*, *String Calculator*, *Bowling Game*).


2. **Estrutura de Pastas por Kata:**
Cada kata deve ter uma estrutura bem definida na raiz do projeto:
```text
katas/
└── kata-01-string-calculator/
    ├── README.md               <-- Apenas o enunciado (o que será enviado à LLM)
    ├── index.js                 <-- Esqueleto/assinatura da função em branco
    └── index.test.js            <-- Suíte de testes com Jest ou Vitest

```


3. **Isolamento e Ocultação dos Testes:**
* **`README.md`:** Contém unicamente a descrição textual do problema (o prompt base que os devs enviarão à LLM no cenário *Com IA*).


* **`index.js`:** Contém apenas a declaração inicial (ex.: `function add(numbers) { return 0; }`).
* **`index.test.js`:** Contém uma bateria abrangente de testes unitários cobrindo todos os cenários do problema. **Importante:** A suíte de testes deve ser mantida oculta da LLM durante os *trials* para garantir que a IA não leia os testes diretamente.




4. **Validação do Setup:**
* Dev 3 testa se rodar `npm test` dentro do diretório de cada kata executa a suíte e se ela falha quando o código está em branco (garantindo que o teste não dê falso-positivo).
