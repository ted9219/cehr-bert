from spark_apps.cohorts.query_builder import QueryBuilder, QuerySpec

COVID_COHORT_QUERY = """
SELECT DISTINCT
    c.person_id,
    FIRST(index_date) OVER (PARTITION BY person_id ORDER BY index_date, visit_occurrence_id) AS index_date,
    FIRST(visit_occurrence_id) OVER (PARTITION BY person_id ORDER BY index_date, visit_occurrence_id) AS visit_occurrence_id
FROM
(
    SELECT DISTINCT
        m.person_id,
        FIRST(measurement_date) OVER (PARTITION BY person_id ORDER BY measurement_date, visit_occurrence_id) AS index_date,
        FIRST(visit_occurrence_id) OVER (PARTITION BY person_id ORDER BY measurement_date, visit_occurrence_id) AS visit_occurrence_id
    FROM global_temp.measurement AS m
    JOIN global_temp.concept AS c
        ON m.value_as_concept_id = c.concept_id
    WHERE m.measurement_concept_id IN (723475,723479,706178,723473,723474,586515,706177,706163,706180,706181)
        AND c.concept_name IN ('Detected', 'Positve')

    UNION

    SELECT 
        co.person_id,
        FIRST(condition_start_date) OVER (PARTITION BY person_id ORDER BY condition_start_date, visit_occurrence_id) AS index_date,
        FIRST(visit_occurrence_id) OVER (PARTITION BY person_id ORDER BY condition_start_date, visit_occurrence_id) AS visit_occurrence_id
    FROM global_temp.condition_occurrence AS co
    WHERE co.condition_concept_id IN (4100065, 37311061)
) c
"""

DEFAULT_COHORT_NAME = 'covid19'
DEPENDENCY_LIST = ['person', 'visit_occurrence', 'measurement', 'condition_occurrence']


def query_builder():
    query = QuerySpec(table_name=DEFAULT_COHORT_NAME,
                      query_template=COVID_COHORT_QUERY,
                      parameters={})
    return QueryBuilder(cohort_name=DEFAULT_COHORT_NAME,
                        dependency_list=DEPENDENCY_LIST,
                        query=query)