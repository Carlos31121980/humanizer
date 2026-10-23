# Respaldo metodológico

Esta skill no crea métodos: aplica métodos reconocidos en la práctica forense y
en la literatura técnica. El informe debe citar el método, no la herramienta.
Claude y los scripts de `scripts/` son el instrumento de cálculo, en el mismo
sentido en que lo sería una planilla Excel, y se mencionan en el informe solo
para efectos de reproducibilidad (los archivos de cálculo se acompañan como
anexo).

Las referencias de abajo se verificaron en su existencia, edición y fecha
el 23-10-2026. Antes de citar un capítulo o página específicos, ábrelos y
confirma el texto, porque los documentos se actualizan.

## 1. Métodos de reconstrucción indirecta de ingresos (módulo A)

| Método | Fuente | Qué dice |
|---|---|---|
| **Patrimonio neto comparado** (*net worth method*) | *Holland v. United States*, 348 U.S. 121 (1954), Corte Suprema de EE.UU. | Valida el método como prueba de ingresos no declarados y fija sus exigencias: el patrimonio inicial debe establecerse "con razonable certeza" (p. 132) y debe haber evidencia de que los incrementos provienen de ingresos gravables, no solo del cálculo. También advierte que el método es una aproximación basada en prueba circunstancial (p. 129) y que la mera subdeclaración no prueba el dolo. |
| Patrimonio neto, gastos, depósitos bancarios y efectivo | IRS, *Internal Revenue Manual*, § 9.5.9 "Methods of Proof" (rev. 29-07-2024) | Describe los métodos indirectos que usa la autoridad tributaria de EE.UU.: *Specific Items, Net Worth, Expenditures* (también llamado *source and application of funds*, el "fuentes y usos" de esta skill), *Bank Deposits, Cash, Percentage Markup, Unit and Volume*. Indica que los tribunales han sostenido los métodos de patrimonio neto, gastos, depósitos bancarios y efectivo. |
| Los mismos métodos, en la práctica profesional | ACFE, *Fraud Examiners Manual* (edición vigente), sección sobre reconstrucción indirecta de ingresos | Manual de referencia de los examinadores de fraude certificados (CFE). Verificar la edición y la sección antes de citar. |
| Norma chilena que presupone el método | Art. 70 y 71 de la Ley sobre Impuesto a la Renta (DL 824) | Presunción de renta igual a los gastos de vida y carga de probar el origen de los fondos de gastos, desembolsos e inversiones. El patrimonio neto comparado es la forma técnica de aplicar esa norma. |

## 2. Pruebas estadísticas y señales de alerta (módulo A)

| Técnica | Fuente | Qué dice |
|---|---|---|
| **Ley de Benford** y umbrales de conformidad | Nigrini, M., *Benford's Law: Applications for Forensic Accounting, Auditing, and Fraud Detection*, Wiley, 2012 | Propone la desviación absoluta media (MAD) como medida de conformidad del primer dígito, con rangos empíricos: 0,000–0,006 conformidad cercana; 0,006–0,012 aceptable; 0,012–0,015 marginal; sobre 0,015 no conformidad. Son criterios empíricos, no valores críticos analíticos: sirven para orientar la revisión, no como prueba. El script `analisis_movimientos.py` usa exactamente esos rangos. |
| **Tipologías y señales de alerta de lavado de activos** | UAF (Chile), *Guía de señales de alerta de LA/FT/FP* (2023) y *X Informe de Tipologías y Señales de Alerta de Lavado de Activos en Chile* (marzo de 2025, sobre 191 sentencias condenatorias 2019–2023) | Catálogo oficial chileno de señales e indicadores. El X Informe identifica, entre otros, el uso de testaferros (79,3 % de los casos), estructuras jurídicas ficticias (48,9 %) y fraccionamiento de operaciones para eludir umbrales (17,4 %). Las señales S-01 a S-30 de esta skill se alinean con esas categorías. |
| Estándares internacionales | GAFI/FATF, *Recomendaciones* y guías de tipologías; GAFILAT para América Latina | Marco del que derivan la Ley 19.913 y las guías de la UAF. |

## 3. Cuantificación de daños en construcción (módulo B)

| Técnica | Fuente | Qué dice |
|---|---|---|
| **Análisis de retraso y disrupción** | Society of Construction Law (Reino Unido), *Delay and Disruption Protocol*, 2ª edición, febrero de 2017 | Referencia internacional en disputas de construcción. Reconoce varios métodos de análisis de retraso y exige elegir el que corresponda a los hechos, los registros disponibles y el momento del análisis; trata la concurrencia de causas, los reclamos globales, la llevanza de registros y los métodos de análisis de disrupción. No tiene fuerza de ley salvo que el contrato lo adopte, pero se usa como referencia técnica. |
| **Análisis forense de programas de obra** | AACE International, *Recommended Practice 29R-03, Forensic Schedule Analysis* (2007; rev. 2011; actualización en curso) | Clasifica los métodos de análisis de retraso basados en CPM y da un vocabulario común. Se declara no prescriptiva: apartarse de ella con fundamento no es por sí un error. Está sometida a debate entre peritos, así que se cita como referencia, no como estándar obligatorio. |
| **Rubros indemnizables** | Código Civil, arts. 1556 (daño emergente y lucro cesante), 1558 (perjuicios previstos e imprevistos), 1559 (intereses), 45 (fuerza mayor) | Marco sustantivo chileno. La clasificación de hechos de `danos-contractuales.md` (mandante, fuerza mayor, reacción del mandante, contratista, concurrente) es la traducción operativa de esas normas. |

## 4. Estándares de la práctica pericial (ambos módulos)

| Principio | Fuente | Qué dice |
|---|---|---|
| Independencia, no subordinar la opinión, no opinar sobre la existencia de fraude como conclusión jurídica, prohibición de honorarios contingentes en ciertos servicios | AICPA, *Statement on Standards for Forensic Services No. 1* (SSFS 1), vigente para encargos aceptados desde el 01-01-2020 | Estándar obligatorio para los contadores públicos de EE.UU. en servicios de litigio e investigación. Esta skill adopta sus principios: separar hechos de conclusiones, no calificar jurídicamente los hechos y declarar supuestos y limitaciones. |
| Integridad de la evidencia y cadena de custodia mediante hash | NIST, *Special Publication 800-86, Guide to Integrating Forensic Techniques into Incident Response* (2006), DOI 10.6028/NIST.SP.800-86 | Describe el proceso forense de identificación, recolección, examen y análisis de datos preservando su integridad y una cadena de custodia estricta; el cálculo de un hash antes y después del examen demuestra que la evidencia no fue alterada. Es lo que hace `inventario_evidencia.py`. |
| Apreciación de la prueba pericial | Art. 132 del Código Tributario (sana crítica: el juez debe expresar las razones "lógicas, científicas, técnicas o de experiencia" que lo convencen) y arts. 409 a 425 del Código de Procedimiento Civil (informe de peritos; el art. 425 remite a la sana crítica) | Exigen que el informe explicite el método y permita seguir el razonamiento. La reproducibilidad de los cálculos de esta skill responde a esa exigencia. Verificar el texto vigente del CPC antes de citarlo. |

## 5. Texto sugerido para la sección "Metodología" del informe

> El análisis se practicó conforme al método de **patrimonio neto comparado**,
> complementado con el estado de **fuentes y usos de fondos** y el **análisis
> de depósitos bancarios**, métodos de reconstrucción indirecta de ingresos
> reconocidos en la práctica forense (IRS, *Internal Revenue Manual* § 9.5.9;
> ACFE, *Fraud Examiners Manual*) y validados jurisprudencialmente
> (*Holland v. United States*, 348 U.S. 121, 1954), que corresponden a la
> lógica de los artículos 70 y 71 de la Ley sobre Impuesto a la Renta. Los
> indicadores de alerta se tomaron de la *Guía de señales de alerta* (2023) y
> del *X Informe de Tipologías* (2025) de la Unidad de Análisis Financiero. La
> integridad de los documentos examinados se resguardó mediante inventario con
> huella digital SHA-256 (NIST SP 800-86). Todos los cálculos se efectuaron con
> procedimientos reproducibles cuyos archivos se acompañan como anexo, de modo
> que cualquier interesado pueda verificar cada cifra desde su documento fuente.

Para el módulo B, reemplaza la primera parte por:

> La cuantificación de perjuicios se practicó identificando cada hecho
> generador, su imputabilidad y su nexo causal con el costo incurrido,
> conforme a los criterios del *Delay and Disruption Protocol* de la Society
> of Construction Law (2ª ed., 2017) y de la *Recommended Practice 29R-03* de
> AACE International para el análisis de retrasos, y a los artículos 1556 y
> siguientes del Código Civil para la determinación del daño emergente y el
> lucro cesante. Se presentan tres escenarios (base, conservador y mínimo)
> para hacer explícita la sensibilidad del resultado a los supuestos adoptados.

Adapta el texto a los métodos que efectivamente usaste. No cites un método que
no aplicaste.
