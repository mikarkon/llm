import os
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_ollama import ChatOllama

def importData():
    import sqlite3

    # creating file path
    dbfile = r'D:\Users\Mikarkon\Documents\contractsALfa.db'
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect(dbfile)

    # creating cursor
    cur = con.cursor()
    strs = ["" for x in range(28)]
    for x in range(1,29):
        sql = f"select client_id, date, crucial_info from contracts where id={x};"
        cur.execute(sql)
        strs[x-1]=cur.fetchall()
    return strs

def createModelForJson():
    from langchain_ollama import ChatOllama
    model = ChatOllama(model="llama3.1:8b", base_url="http://127.0.0.1:11434", format = 'json')
    system_mes = """
    YOU ARE THE WROLD'S BEST EXRTACTOR OF STATISTIC'S INFO INTO JSON FORMAT.
    YOUR TASK IS TO ANALYZE THE GIVEN CONTRACTS' INFO AND EXTRACT KEY DETAILS, PRESENTING THEM IN A JSON FORMAT.
    ###ISNTRUCTIONS###
    - ANSWER IS A JSON OBJECT.
    - EXTRACT and PRESENT the following contract details in JSON format:
        - 'Client'
        - 'Date'
        - 'Total Cost'
    - ENSURE the JSON data is well-structured and follows the exact field names provided.
    
    ###CHAIN OF THOUGHTS###
    1. Reading the each Contract:
       1.1. Carefully read the entire text to identify key details.
       1.2. Pay special attention to sections mentioning client name and costs.
       1.3. Focus on words like 'Общая стоимость услуг:', 'Общая сумма вознаграждения:', 'Общая стоимость выполненных услуг:'.
       1.4. Find the client name in each contract that is the first word in ''.
       1.6. Find the date it is in the second '' but get only the numbers seperated by '.', ignore '___'
       1.5. Find the total cost the biggest numeric that is given in a format like '10 000, 00 рублей' and interpret it as a normal number.
    
    2. Extracting Information:
       2.1. Identify and extract the 'Client' name.
       2.2. Find and extraxt the 'Date' without '__' symbols.
       2.3. Find and extract the 'Total Cost' involved it is always the biggest number of money.
    
    3. Formatting as JSON:
       3.1. Organize the extracted details into a JSON structure.
       3.2. Ensure that each field matches the exact names provided.
       
    ###NOT TO DO###
    - NEVER ADD ANY EXTRA WORDS BEFORE OR AFTER THE ANSWER
    - NEVER ADD ANY TEXT THAT WAS NOT GIVEN
    - NEVER PROVIDE DATA IN ANY FORMAT OTHER THAN THE SPECIFIED JSON STRUCTURE.
    - NEVER PUT '____' IN DATE PART
    
    ###EXAMPLE CONTRACT JSON OUTPUT###
    
    ```json
    
        Client: None,
        Date: None,
        Total Cost: None
    """
    template = ChatPromptTemplate([
    ("system", system_mes),
    ("human", """('Alfa-Bank', '___ __.____.2019', 'Вот ключевая информация из представленного контракта:\n
    1. **Стороны договора**:\n   - Заказчик: АО «АЛЬФА-БАНК», представители: Руководитель Дирекции процессинга Брынин Сергей Вячеславович.\n   - Исполнитель: ООО «БПЦ Банковские Технологии», представители: Генеральный директор Бубнов Дмитрий Владимирович.\n
    2. **Предмет заказа**:\n   - Установка и настройка обновленной версии Ядрового ПО SVFE, SVBO для упрощения авторизации сотрудников при внесении наличных денег в банкоматы.\n
    3. **Стоимость и оплата**:\n   - Общая стоимость услуг: 550 000,00 рублей, включая НДС 20% (91 666,00 рублей).\n   - Аванс 20%: 110 000,00 рублей, включая НДС 20% (18 333,00 рублей), выплачивается в течение 10 рабочих дней после подписания.\n   - Окончательный расчет 80%: 440 000,00 рублей, включая НДС 20% (73 333,00 рублей), выплачивается в течение 10 рабочих дней после подписания акта сдачи-приемки услуг.\n
    4. **Вступление в силу и действие**:\n   - Заказ вступает в силу с момента его подписания обеими сторонами и является частью Рамочного договора № С8463 от 09 января 2018 года.\n
    5. **Календарный план оказания услуг**:\n   - Не указан подробный календарный план в тексте, предполагается предоставление после согласования сторон.\n
    6. **Приложение**:\n   - Обозначено важное приложение — FSD, содержащее подробные требования заказчика к системе SmartVista.\n
    7. **Особые условия**:\n   - Статья 823 ГК РФ не применяется к отношениям сторон по данному договору.'),"""),
    ("ai", """{{"Client": "Alfa-Bank", "Date":"2019", "Total Cost" : 550000}}
    """),
    ("human", """('Alfa-Bank', '09.01.2018', 'Из представленного контракта можно выделить следующую ключевую информацию:\n
    1. **Спецификация № 57 к Лицензионному договору № С8464 от 09 января 2018 г.**:\n   - Дата составления: «___» ____________ 2019 г.\n   - Местоположение: Москва.\n
    2. **Лицензиат**:\n   - Организация: АО «АЛЬФА-БАНК».\n   - Представитель: Руководитель Дирекции процессинга Брынин Сергей Вячеславович.\n   - Основание действия: доверенность № 4/1712Д от 10.06.2019 г.\n
    3. **Лицензиар**:\n   - Организация: ООО «БПЦ Банковские Технологии».\n   - Представитель: Генеральный директор Бубнов Дмитрий Владимирович.\n   - Основание действия: Устав.\n
    4. **Предмет Спецификации**:\n   - Лицензиар обязуется предоставить Лицензиату право использования обновленной версии Ядрового ПО SVFE, SVBO «Изменение бух.учета по предоплаченным картам» (в соответствии с требованиями ЦБ РФ по предоплаченным картам в рамках 579-П).\n
    5. **Вознаграждение и порядок оплаты**:\n   - Общая сумма вознаграждения: 1 500 000,00 рублей, не облагается НДС в силу пп.26 п.2 ст.149 НК РФ.\n   - Аванс: 20% от общей суммы, 300 000 рублей, оплата в течение 10 рабочих дней после подписания Сторонами Заказа.\n   - Окончательный расчет: 80% от общей суммы, 1 200 000 рублей, оплата в течение 10 рабочих дней после подписания Сторонами Акта сдачи-приемки ПО и Акта сдачи-приемки оказанных услуг по Заказу № 57.\n
    6. **Юридическая сила**:\n   - Спецификация составлена в двух экземплярах, имеющих одинаковую юридическую силу, по одному для каждой из Сторон.\n\nЭти данные предоставляют краткий обзор документа и его основных положений, что полезно для анализа и дальнейшего использования.'),"""),
    ("ai", """{{"Client": "Alfa-Bank","Date":"09.01.2018", "Total Cost" : 1500000}}
    """),
    ("human","""[('Alfa-Bank', '09.01.2018', '**Ключевая информация из акта сдачи-приемки к Рамочному договору № С 8463 от 09 января 2018 г.:**\n
    1. **Стороны:**\n   - Исполнитель: ООО «БПЦ Банковские Технологии» (Генеральный директор — Бубнов Дмитрий Владимирович).\n   - Заказчик: АО «АЛЬФА-БАНК» (Руководитель Дирекции процессинга — Брынин Сергей Вячеславович, доверенность № 4/641Д от 14.03.2019 г.).\n
    2. **Предмет акта:**\n   - Услуги по установке и настройке Обновленной версии Ядрового ПО SVFE, SVBO «Упрощение авторизации сотрудников МДО/ККО в банкоматах при внесении наличных денег».\n
    3. **Стоимость и оплата:**\n   - Общая стоимость выполненных услуг: 550 000,00 рублей, включая НДС 20% (91 666,66 рублей).\n   - Ранее выплаченный аванс: 110 000,00 рублей, включая НДС 20% (18 333,33 рублей).\n   - Сумма к оплате по акту: 440 000,00 рублей, включая НДС 20% (73 333,33 рублей).\n
    4. **Услуги:**\n   - Исполнитель выполнил услуги в полном объеме, с надлежащим качеством, в установленный договором срок.\n
    5. **Заключение:**\n   - После оплаты вышеуказанных услуг стороны не будут иметь претензий друг к другу в рамках договора и соответствующего заказа.\n\n**Дата и место:** \n- Город Москва, дата акта не указана.')] """),
     ("ai", """{{"Client": "Alfa-Bank","Date":"09.01.2018", "Total Cost" : 550000}}
    """),
    ("human", "{user_input}"),
    ])
    chain = template | model
    return chain

def transformToJson(chain, strs):
    ans= ["" for x in range(28)]
    for x in range(28):
        ans[x]+=chain.invoke({"user_input": strs[x]}).content
    ans_text='['
    for x in range(28):
        ans_text += ans[x]
        ans_text+=','
    ans_text = ans_text[:-1]
    ans_text+=']'
    ans_text=ans_text.replace("__ .__.", "") 
    ans_text=ans_text.replace("___ _____________ ", "")
    ans_text=ans_text.replace("__ ___________ ", "")
    ans_text=ans_text.replace("___.___", "")
    return ans_text
    
async def asyncTransformToJson(chain, strs):
    ans= ["" for x in range(28)]
    for x in range(28):
        async for text in chain.astream({"user_input":strs[x]}):
            print(text.content, end="", flush=True)
            ans[x]+=text.content
    ans_text='['
    for x in range(28):
        ans_text += ans[x]
        ans_text+=','
    ans_text = ans_text[:-1]
    ans_text+=']'
    ans_text=ans_text.replace("__ .__.", "") 
    ans_text=ans_text.replace("___ _____________ ", "")
    ans_text=ans_text.replace("__ ___________ ", "")
    ans_text=ans_text.replace("___.___", "")
    return ans_text
    
def createModelForPlot():
    model1 = ChatOllama(model="llama3.1:8b", base_url="http://127.0.0.1:11434")
    system_mes = """
    YOU ARE THE WORLD'S BEST PYTHON CODE WRITER.
    YOUR TASK IS TO WRITE CODE IN PYTHON USING MATPLOTLIB TO GET A CHART FOR THE GIVEN INFO
    MAKE CHART THAT WILL HAVE LABELS OF EACH VALUE on x-axis
    ###ISNTRUCTIONS###
    - ANSWER IS A CODE IN PYTHON
    - ANALYZE GIVEN INFO IN JSON FORMAT FOR BUILDING A CHART
    - ENSURE YOUR CODE IS RUNNABLE
    
    ###CHAIN OF THOUGHTS###
    1. Analyzing given data:
       1.1. Carefully read the entire json object to identify key details.
       1.2. Based on the provided question identify y-axis and x-axis.
       1.3. You must make a chart where each JSON object in a given array has its own bar
    2. Creating a chart:
       2.1. Use xticks() function to make labels on x-axis for each value 
    """
    template1 = ChatPromptTemplate([
    ("system", system_mes),
    
    ("human", "{user_input}"),
    ])
    chain1 = template1 | model1
    return chain1

def transformToPlot(chain1, ans_text, question):
    question+='\n'
    question+=ans_text
    code=''
    code+=chain1.invoke({"user_input": question}).content
    return code
    
async def asyncTransformToPlot(chain1, ans_text, question): 
    question+='\n'
    question+=ans_text
    code=''
    async for text in chain1.astream({"user_input":question}):
        print(text.content, end="", flush=True)
        code+=text.content
    return code
    
def resultDbToCode(question):
    strs = importData()
    chain = createModelForJson()
    ans_text = transformToJson(chain, strs)
    chain1 = createModelForPlot()
    code = transformToPlot(chain1, ans_text, question)
    return code

async def asyncResultDbToCode(question):
    strs = importData()
    chain = createModelForJson()
    ans_text = await asyncTransformToJson(chain, strs)
    chain1 = createModelForPlot()
    code = await asyncTransformToPlot(chain1, ans_text, question)
    return code