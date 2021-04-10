---
title: "Excel Basics"
date: "07-04-2021"
categories:
  - Personal
tags:
  - Personal
  - Excel

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

Using the fill handle and dragging across cells, Excel will automatically fill in blanks will associated formulas. This is called relative reference and allows us to quickly auto-fill cells with desired formulas. However, there will be times where will do not want this to occur. How this will achieved will be covered later

|![relative reference](/assets/images/personal-excel-basics/rel_ref-1.png)<br><em>relative reference</em>|![relative reference op](/assets/images/personal-excel-basics/rel_ref-2.png)<br><em>relative reference output</em>|

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

Other capabilities of Excel 2019

***
As the remaining fx of have little relation with each other, I will summarise the things I have learnt in point form from here onwards. 

- Apparently Excel 2019 supports up to 16,384 columns by 1,048,576 rows per sheet.

- ![cell nav](/assets/images/personal-excel-basics/cell_nav.png)<br>
  This box can be used to jump to any cell by keying in the coordinates

- ![find and replace](/assets/images/personal-excel-basics/find_replace.png)<br>
  Find and replace fx, arguably more important than in Word

**Notice** From this point onwards, I will be using a spreadsheet provided by SP for MS4215 : 
Statistics and Analytics for Engineers
{: .notice--warning}

- ![freeze](/assets/images/personal-excel-basics/freeze.png)<br>
  Freezing panes allows us to keep the desired colum when navigating the sheet.



![WIP](/assets/images/common/WIP.png)