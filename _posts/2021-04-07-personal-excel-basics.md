---
title: "Excel Basics"
date: "10-04-2021"
categories:
  - Learning process
tags:
  - Excel
  - Learning process

---
**Microsoft Excel** Microsoft Excel is a spreadsheet software featuring various tools like pivot tables and a macro programming language called Visual Basic for Applications(VBA).
{: .notice--info}

**Libre Office - Calc Spreadsheets** Calc Spreadsheets is a Free and Open Source (FOSS) alternative to Excel. Each has it's strengths and weaknesses, which can be found <a href="https://wiki.documentfoundation.org/Feature_Comparison:_LibreOffice_-_Microsoft_Office#Spreadsheet_applications:_LibreOffice_Calc_vs._Microsoft_Excel">here. <a>
{: .notice--info}

***

Introductions

***

Excel is a powerful tool that is used in almost every industry. As such. I believe it is appropriate that I learn a thing or 2 that I am almost guaranteed to be using sometime in the future. 

For this brief introduction, I will be using the following video: <a href="https://www.youtube.com/watch?v=ZNGqeCcTu0Q">
Microsoft Excel Tutorial: 3-Hour MS Excel 2019 Course for Beginners!<a> <a href ="https://www.youtube.com/channel/UC-3e3hAUhDV2lwcoQGD2grg">by the channel: Simon Sez IT </a>.  

***

Basic formulas and operations

***

The first 30 minutes of the video goes through various aspects of the interface of Excel 2019, hence I will be skipping ahead.

The use of basic formulas are outline in the table below

| Action and Command     | Image |
| ----------- | ----------- |
| Addition<br><br>Use: <strong>+</strong>|![add](/assets/images/personal-excel-basics/add.png)<br><br>![add op](/assets/images/personal-excel-basics/add_op.png)<br><em>addition output</em>|
| Subtraction<br><br>Use: <strong>-</strong>|![minus](/assets/images/personal-excel-basics/minus.png)<br><br>![minus op](/assets/images/personal-excel-basics/minus_op.png)<br><em>subtraction output</em>|
| Multiplication<br><br>Use: <strong>*</strong>|![multiply](/assets/images/personal-excel-basics/multi.png)<br><br>![multiply op](/assets/images/personal-excel-basics/multi_op.png)<br><em>multiply output</em>|
| Division<br><br>Use: <strong>/</strong>|![divide](/assets/images/personal-excel-basics/divide.png)<br><br>![divide op](/assets/images/personal-excel-basics/divide_op.png)<br><em>division output</em>|
| Power<br><br>Use: <strong>^</strong>|![power](/assets/images/personal-excel-basics/pwr.png)<br><br>![power op](/assets/images/personal-excel-basics/pwr_op.png)<br><em>power output</em>|
| Precedent<br><br>Use: <strong>( )</strong>|![precedent](/assets/images/personal-excel-basics/precedent.png)<br><br>![precedent op](/assets/images/personal-excel-basics/precedent_op.png)<br><em>precedent output</em>|
|<em>All formula must have an '=' at the front</em>| |

Regarding precedent, the order of operations for Excel is as follows:

1. : ( )
2. : ^
3. : * /
4. : + -

Other wise, the formula will be executed from left to right. 

<strong>Relative reference</strong>

Using the fill handle and dragging across cells, Excel will automatically fill in blanks will associated formulas. This is called relative reference and allows us to quickly auto-fill cells with desired formulas. However, there will be times where will do not want this to occur. To achieve this, we use an operation called absolute values.

|![relative reference](/assets/images/personal-excel-basics/rel_ref-1.png)<br><em>relative reference</em>|![relative reference op](/assets/images/personal-excel-basics/rel_ref-2.png)<br><em>relative reference output</em>|

<strong>Absolute Values</strong>

By inserting '$' between coordinates of the cells, we can indicate that cell as an absolute value. This allows us to use relative reference without worrying about generating inaccurate values.

| Action and Command     | Image |
| ----------- | ----------- |
|Using relative reference without absolute values|![relative ref, no absolute val](/assets/images/personal-excel-basics/abs_val-1.png)<br><br>![relative ref, no absolute val 2](/assets/images/personal-excel-basics/abs_val-2.png)<br><em>relative value giving inaccurate results</em>|
|Using relative reference with absolute values|![relative ref,with absolute val](/assets/images/personal-excel-basics/abs_val-3.png)|


<strong>Ranges</strong>

Ranges are groups of adjacent cells that the user wants to work with. The user define ranges by dragging and highlighting the desired cells. 

Other methods of definition include:
1. Clicking a cell, holding the 'shift' key and clicking another cell
2. By using a : between 2 desired cells. For example B2:C4

![range](/assets/images/personal-excel-basics/range-1.png)

It is important to note that only 'enter' and 'tab' keys are to be used when navigating ranges.The white cell in the range denotes a highlighted cell. Using the arrow key will de-select the range and navigate to another cell, ditto for mouse clicking.

Information of the selected range can also be found at the bottom of the Excel UI.

![range stats](/assets/images/personal-excel-basics/range-stat.png)

<strong>Linking information from different sheets</strong>
Using the syntax: ='sheet_name'!cell_number, values of one sheet can be called from another sheet.

|![sheet call](/assets/images/personal-excel-basics/sheet.png)<br><em>Focus on cell B3</em>|![sheet call op](/assets/images/personal-excel-basics/sheet_op.png)<br><em>Cell B3 of sheet 1  called from another sheet</em>|

***

Formulas and Functions

***
**Notice** From this point onwards, I will be using a spreadsheet provided by SP for MS4215 : Statistics and Analytics for Engineers
{: .notice--warning}

Functions are words in formulas that specify its operations. Excel has a variety of formulas for different use cases, all of which can be found here: <a href="https://support.microsoft.com/en-us/office/excel-functions-by-category-5f91f4e9-7b42-46d2-9bd1-63f26a86c0eb">Excel functions (by category) </a>. For this post, I will only go through the top 10 most popular functions according to Microsoft.

<strong>Top 10 functions in excel</strong>

| Function    | image |
| ----------- | ----------- |
| <strong>SUM</strong> <br>Used to add values,<br> cell references, range<br> or a mix of the 3 | ![SUM](/assets/images/personal-excel-basics/sum.png) |

| <strong>IF</strong> <br>Used to make logical comparison | ![IF](/assets/images/personal-excel-basics/if.png)<br><em>IF function with relative reference</em>|

| <strong>LOOKUP</strong> <br>Used to find values<br> in a single row or column<br> and return a corresponding<br> value in another row or<br> column| ![LOOKUP](/assets/images/personal-excel-basics/lookup.png)<br><em>Look up '62' from column B and return the value from column C</em>|

| <strong>VLOOKUP</strong> <br>Used to find things in a table| ![LOOKUP](/assets/images/personal-excel-basics/vlookup.png)<br><em>Look up the value of B6 from column B and return the number of times 45 appears</em>|

| <strong>MATCH</strong> <br> Used to search for<br> specified items in a<br> range of cells, then<br> returns the relative position of that item<br> in the range.| ![MATCH](/assets/images/personal-excel-basics/match.png)<br><em>Look up the amount of times 'IT/Eng' from column B and return the number of times it appears</em>|

| <strong>CHOOSE</strong> <br> An alternative to<br> VLOOKUP and IF functions| ![CHOOSE](/assets/images/personal-excel-basics/choose.png)<br><em>Using CHOOSE and relative reference to assign colours, credit to:<a href="https://www.youtube.com/watch?v=UkEItMh2Vs4">How to use the CHOOSE function</a> </em>|

| <strong>DATE</strong> <br> Excel has a DATE function<br> that lets user input dates.<br> However, I prefer to use<br> the TODAY() function as<br> it is more efficient| ![DATE](/assets/images/personal-excel-basics/date-1.png)<br><em>Using TEXT and DATE function to format a and relative reference to assign colours</em><br><br>![DATE](/assets/images/personal-excel-basics/date-1.png)<br><em>Using TEXT and TODAY function to automatically generate the date</em>|

| <strong>DAYS</strong> <br> Returns number of days between 2 dates| ![DAYS](/assets/images/personal-excel-basics/days.png)<br><em>Finding the number of dates between 11 April 2021 and 31 December 2021</em>|

| <strong>FIND</strong> <br> Finds the location of a substring in a string | ![CHOOSE](/assets/images/personal-excel-basics/find_fx.png)<br><em>Finding positions. credit to:<a href="https://www.youtube.com/watch?v=NVeAPVP8zWg">How to use the FIND function in Excel</a> </em>|

| <strong>INDEX</strong> <br> Used to return a value or the reference to a value from  a table or range. | ![INDEX](/assets/images/personal-excel-basics/index.png)<br><em>Index function<a href="https://www.youtube.com/watch?v=U6OMmXgAWJc">How to use the INDEX function in Excel</a> </em>|

***

Printing an Excel spread sheet

***

Header and footers can be inserted when an excel sheet needs to be printed. There are options to change to the 'Header and Footer' view from either the top menu bar or the bottom left.

|![header and footer top](/assets/images/personal-excel-basics/header_footer_top.png)|
|<em>Top bar, under 'insert' tab</em>|
|![header and footer bottom](/assets/images/personal-excel-basics/header_footer_bottom.png)|
|<em>Bottom left button|

|![header and footer view](/assets/images/personal-excel-basics/header_footer_view.png)|
|<em>Header and footer on display</em>|

A contextual tab will appear when working with the header and footer. The tab is filled with options that one will fine useful when formatting documents. Cells can also be resized to better fit desired dimensions. The contextual tab when the user clicks away from the header and footer. Simply click on the header or footer again for the tab to re-appear.

Any addition made to a header and footer of one page will automatically be copied to all pages. Using the options in the contextual tab will allow for automatic updating of elements.

|![header and footer top eg](/assets/images/personal-excel-basics/header_footer_top_eg.png)|
|<em>Header, manually typed</em>|
|![header and footer bottom eg](/assets/images/personal-excel-basics/header_footer_bottom_eg.png)|
|<em>Footer, inserted with contextual tap</em>|
|![header and footer top eg](/assets/images/personal-excel-basics/header_footer_bottom_eg_op-1.png)|
|<em>Footer output, auto-generated, page 1</em>|
|![header and footer top eg](/assets/images/personal-excel-basics/header_footer_bottom_eg_op-2.png)|
|<em>Footer output, auto-generated, page 2</em>|

To ensure that individual pages have the proper headings or columns, we need to use the 'print title' option under the 'page layout' tab.

|![print title options](/assets/images/personal-excel-basics/print_title.png)|
|<em>print title options</em>|
|![print title before](/assets/images/personal-excel-basics/print_title_before.png)|
|<em>before print title</em>|
|![print title before](/assets/images/personal-excel-basics/print_title_after.png)|
|<em>after print title</em>|

<strong>Comments, notes and printing both in excel</strong>

Similar to programming languages, comments can be inserted into excel.

|![insert comment 1](/assets/images/personal-excel-basics/comment_insert-1.png)|![insert comment 2](/assets/images/personal-excel-basics/comment_insert-2.png)
|<em>methods of inserting comment</em>|
|![insert comment op](/assets/images/personal-excel-basics/comment_insert_op.png)|![insert comment op 2](/assets/images/personal-excel-basics/comment_insert_op-2.png)
|<em>working with comments</em>|

To print the comment, we use the same menu as the one we used to set our header and footer.

|![comment print setup](/assets/images/personal-excel-basics/comment_print.png)|
|<em>comment printing setup</em>|
|![comment print output](/assets/images/personal-excel-basics/comment_print_op.png)|
|<em>comment print preview</em>|

Notes are similar in nature with comments. Except note do not have collaboration tools and require hovering over it to view it (or the user can use the top bar to navigate notes).

|![insert note 1](/assets/images/personal-excel-basics/note_insert-1.png)|![insert note 2](/assets/images/personal-excel-basics/note_insert-2.png)
|<em>methods of inserting notes</em>|
|![insert note op](/assets/images/personal-excel-basics/note_insert_op.png)|![insert note op 2](/assets/images/personal-excel-basics/note_insert_op-2.png)
|<em>viewing notes</em>|

To print notes, we use the same menu as the one we used to set our header and footer.

|![note print setup](/assets/images/personal-excel-basics/note_print.png)|
|<em>note printing setup</em>|
|![note print output - end](/assets/images/personal-excel-basics/note_print_op-1.png)|
|<em>printing notes at the end of the document</em>|
|![note print output - displayed](/assets/images/personal-excel-basics/note_print_op-2.png)|
|<em>printing notes as displayed</em>|

Other than those mentioned above, Excel has many different options that allows the user to adjust their spread sheet for printing

|![print settings](/assets/images/personal-excel-basics/print_settings.png)|
|<em>page layout tab</em>|


***

Other capabilities of Excel 2019

***
As the remaining function of have little relation with each other, I will summarise the things I have learnt in point form from here onwards. 

- Apparently Excel 2019 supports up to 16,384 columns by 1,048,576 rows per sheet.

- ![cell nav](/assets/images/personal-excel-basics/cell_nav.png)<br>
  This box can be used to jump to any cell by keying in the coordinates

- ![find and replace](/assets/images/personal-excel-basics/find_replace.png)<br>
  Find and replace function, arguably more important than in Word

- ![freeze](/assets/images/personal-excel-basics/freeze.png)<br>
  Freezing panes allows us to keep the desired colum/row when navigating the sheet.

- ![split](/assets/images/personal-excel-basics/split.png)<br>
  Splits the sheet into 2 sets of sheets, allowing viewing of 2 places at once.

- ![transpose](/assets/images/personal-excel-basics/transpose.png)<br><br>![transpose](/assets/images/personal-excel-basics/transpose_op.png)<br>
  Transpose switches the values of columns and rows


