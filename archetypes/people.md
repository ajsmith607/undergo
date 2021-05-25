
---
title: "{{ (replace (replace .Name "_" " ") "-" " ") | title }}"

date: {{ dateFormat "2006-01-02" .Date }}
date_x:                     # integer that indicates precision of date, see below
_date:                      # override display of date 
_date_f:                    # formatting of override display, default to plain text
publishdate: {{ dateFormat "2006-01-02" .Date }}
draft: false

tags: 

    
person:
  born:                     # YYYY-MM-DD
  born_x:                   # integer that indicates precision of date, see below
  _born:                    # override display of date 
  _born_f:                  # formatting of override display, default to plain text
  birthplace:
  died:                     # YYYY-MM-DD
  died_x:                   # integer that indicates precision of date, see below
  _died:                    # override display of date 
  _died_f:                  # formatting of override display, default to plain text
  deathplace:
  parents:
  - name:                   # firstname middlename lastname  
    birthyear:
    role:                   # father mother step-mother etc
  partners:
  - name:                   # firstname middlename lastname 
    birthyear:
    married:
    children:
    - name:                 # firstname middlename lastname 
      birthyear:
      types:                # daughter, step-son, adopted, etc. | seperate multiple with comma
  siblings:
  - name:
    birthyear:
    type:                   # brother, step-sister, twin, etc. | seperate multiple with comma
  others:
  - name: 
    birthyear:
    relat:
  interred_at: 
    name:
    lat:                    # of grave site, not cemetery
    lon:                    # of grave site, not cemetery
    plot_desk:
    display: 
  aliases:
  -

CONVENTIONS: >

Filenames follow this convention to (hopefully) uniquely identify them, easily sort and still be fairly human-readable: 
  lastname-firstname-middlename_birthyear.md

Featured image:
  To use, add an image named `featured.jpg/png` to your page's folder. 

Index these fields only:
  - title
  - tags (would include locations, affiliations, events, etc.)
  - mother, father, spouse, sibling (children are unnecessary)

Dates:
  Problem: Date data is supplied in a variety of formats and specificity. We need a uniform way to store dates so they:
    - are human-readable, 
    - sort as expected,
    - can be queried in a natural way,
    - allow date arithmetic,
    - can be transformed and dispLayed flexibly, 
    - can also handle "fuzzy" dates such as dates with unknown information as well as formats like "Spring 2021", 
    - is in a storage agnostic format so it is still usable in the future.

  Solution:
    - store dates in a typical date storage format such as a text string using the convention: YYYY-MM-DD,
    - if the exact date is unknown, store it at the start of the period indicated by the known granularity of the date, and 
    - include an optional field that is an integer indicating the (closest) level of specificity/accuracy of the date:
        - 1 = exact date (default), 
        - 2 = month, 
        - 3 = year.
    - use simple conditional logic to display appropriately.

    Examples: 
      - given: "2021":
          - store as: "2021-01-01"
          - specificity: 3
      - given: "Spring 2021"
          - store as: "2021-03-20"
          - specificity: 2 # perhaps the "closest" or most natural in terms of sorting, etc.
      - given: "May 2021":
          - store as: "2021-05-01"
          - specificity: 2
      - given: "May 6th, 2021"
          - store as: "2021-05-06"
          - specify: 1 # can be left unspecified and assumed as the default value 

    Additional flexibility is provided by an optional free text date display field that can be used to override normal display logic for situations like the "Spring 2021" example given above. For further sophistication, a fourth optional field can indicate the format of the display override field, allowing for formatting such as HTML, a regular expression, a formatted string with placeholders, or a function callback (including things like a URL to an API), to name a few obvious examples. This fourth field is obviously overkill for most applications.

  Implementation: using date of birth as an example:
    -  born:       # YYYY-MM-DD
    -  born_x:     # integer that indicates precision of date
    -  _born:      # override display of date 
    -  _born_f:    # formatting of override display, default to plain 

    If I know that someone was born in May 2021, I would store it as:
      - born = "2021-05-01"
      - born_x = 2
    
    Conditional display logic will reflect back the original "May 2021" but circumstances might be such that I want to add this metadata (and the corresponding display logic to use it):
      - _born = "May 2021 <note>(possibly on the 6th?)</note>"
      - _born_f = "xml"
    
  This proposed approach to handling dates will not account for every situation that might be encountered, but I believe that even just using the first pair of fields to store date information (as in the example above of born and born_x fields) will account for the most common situations encountered.

---


<!--more--> 

## Birth

## Geneology

## Known Aliases

## Known Associates

## Education

## Occupations

## Affiliations

## Associated Locations

## Death

## Misc.

## Open Questions

## Speculative/Unproven/Facts In Doubt

## Notes For Researchers

## Bibliography



