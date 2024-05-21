## <p align="center">Personalities from Biographies</p>

**<p align="center">Muhua Huang, Max Zhu</p>**
**Abstract**

Our project aims to use computational techniques to explore the Big Five personalities of historical and public figures
through
their biographies. We will employ
the [HuggingFace personality detection API](https://huggingface.co/Minej/bert-base-personality)
to extract Big Five personality scores from biographical texts. This approach will provide a novel, quantitative measure to examine the personalities of notable individuals, assisting social scientists in understanding their behaviors and impacts within their respective contexts. The application supports input in PDF, TXT, and EPUB formats. While it is recommended to upload autobiographies for better interpretability, the system can process any document that meets the file type requirements.

**Social Science Significance**

The personalities of public figures often remain enigmatic despite their profound influence on history and culture. By
quantifying personality traits from autobiographies, we can offer social scientists a tool to decode complex behaviors
and identify patterns and trends across different eras.

The Big Five theory, which posits that human personality can be distilled into five broad dimensions—Openness,
Conscientiousness, Extraversion, Agreeableness, and Neuroticism—provides a robust framework for this analysis. These
dimensions have been extensively validated and are widely accepted in psychology for their ability to describe and
predict individual differences in behavior and cognition. Understanding these traits in historical and public figures
can reveal how personality influences leadership styles, decision-making processes, and social interactions.

By applying the Big Five theory to biographical texts, we can systematically analyze the personality traits of
influential individuals. This quantitative approach complements traditional qualitative assessments, providing a more
comprehensive understanding of the factors that drive historical and cultural shifts. For instance, examining the high
levels of Openness and Conscientiousness in certain leaders might explain their innovative policies and meticulous
governance. Similarly, high levels of Extraversion and Agreeableness could be linked to charismatic leadership and
successful diplomacy.

This systematic analysis enables researchers to draw correlations between personality traits and significant social
phenomena, offering new insights into the role of individual dispositions in shaping the course of history. Moreover, it
allows for cross-cultural comparisons and the identification of universal traits associated with effective leadership
and influence. The ability to analyze personalities on a large scale provides valuable data for constructing theories
about the impact of personality on historical events and cultural trends.

**Justification for Using Scalable Computing Methods**

The scale of biographical data available for analysis is vast, encompassing thousands of texts spanning various
historical periods and cultures. Manual analysis of such a volume of data is impractical and time-consuming. Therefore,
leveraging scalable computing methods is crucial for efficiently processing and analyzing these texts. High-performance
computing (HPC) allows for the simultaneous processing of multiple texts, significantly reducing the time required for
data extraction and analysis. Additionally, HPC enables the handling of large datasets, ensuring that the analysis is
comprehensive and inclusive of diverse sources. By employing scalable computing methods, we can ensure the robustness
and reliability of our findings, making them more applicable and valuable to social science research.

**Methodology and High-Performance Computing Strategy**:

1. Parallel Processing: To handle the large volume of biographical texts, we will utilize parallel processing
   techniques.
   This will involve deploying a `step function` in AWS to manage multiple `Lambda worker` nodes that can handle
   parallel API calls efficiently. By distributing the workload across multiple processors, we can achieve significant
   speed-ups in data processing and reduce the overall time required for analysis.

2. Result Aggregation: We will implement different aggregation strategies based on the size of the input data. For small
   datasets, `serial processing` will be sufficient. However, for larger datasets, we will use numba, a just-in-time
   compiler for Python, to parallelize the processing tasks. This will enhance the performance of our computations,
   allowing us to handle larger volumes of data more efficiently.

3. Data Management: Effective data management is essential for the success of our project. We will store the extracted
   personality data, along with the corresponding book titles and names of the individuals, in a `relational database
   system (RDS)`. This approach will prevent redundant computations and streamline data retrieval, making the system more
   efficient. Additionally, we will store the raw text files in `Amazon S3` for record-keeping and backup purposes. This
   dual approach ensures data integrity and accessibility while maintaining the scalability of the system.

4. User Interface: To facilitate user interaction with the data, we will develop a frontend dashboard hosted on an AWS
   `EC2 server`. The dashboard will be built using streamlit, a framework that allows for the rapid development of
   interactive web applications. This user-friendly interface will enable multiple users to access the service
   simultaneously, explore the data, and gain insights from the personality analysis. The real-time interaction
   capability of the dashboard will enhance the usability and accessibility of the system, making it a valuable tool for
   social scientists and researchers.