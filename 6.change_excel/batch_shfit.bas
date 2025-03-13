Sub ProcessAllWorkbooks()
    Dim wb As Workbook
    Dim ws As Worksheet
    Dim folderPath As String
    Dim file As String
    
    ' 设置要处理的工作簿所在的文件夹路径
    folderPath = "C:\\Users\\user\\Desktop\\service-\\vba_test\\" ' 请替换为实际路径
    
    ' 获取文件夹中的第一个 Excel 文件（支持 .xlsx 和 .xls）
    file = Dir(folderPath & "*.xlsx")
    
    ' 循环处理文件夹中的每个文件
    Do While file <> ""
        On Error GoTo ErrorHandler ' 添加错误处理
        
        ' 打开工作簿
        Set wb = Workbooks.Open(folderPath & file)
        
        ' 检查是否有名为 "Sheet1" 的工作表
        On Error Resume Next
        Set ws = wb.Worksheets("Sheet1") ' 目标工作表名称
        On Error GoTo 0
        
        If Not ws Is Nothing Then
            ' 调用 ModifySheetContents 子程序来处理该工作表
            Call ModifySheetContents(ws)
        Else
            MsgBox "工作簿 " & file & " 中未找到 'Sheet1' 工作表!", vbExclamation
        End If
        
        ' 保存并关闭工作簿
        wb.Close SaveChanges:=True
        
        ' 获取下一个文件
        file = Dir
        GoTo ContinueLoop ' 跳过错误处理
        
ErrorHandler:
        MsgBox "处理文件 " & file & " 时出错：" & Err.Description, vbCritical, "错误"
        If Not wb Is Nothing Then
            wb.Close SaveChanges:=False ' 出错时不保存
        End If
        
ContinueLoop:
    Loop
    
    MsgBox "所有工作簿处理完成！"
End Sub

Public Sub ModifySheetContents(ws As Worksheet)
    On Error GoTo ErrorHandler
    
    Dim lastRow As Long
    Dim lastCol As Long
    Dim i As Long, j As Long
    Dim rowContainsKeyword As Boolean
    Dim currentDate As String
    
    ' 获取当前日期，格式为 yyyy/mm/dd
    currentDate = Format(Date, "yyyy/mm/dd")
    
    ' 获取工作表的最后一行和最后一列
    '  为了扩大作用范围多了10个单元格的行和列
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row + 10 
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column + 10
    MsgBox "" & lastRow
    MsgBox "" & lastCol
 
    
    ' 功能 1：遍历每一行
    For i = 1 To lastRow
        rowContainsKeyword = False
        
        ' 检查当前行是否包含 "mojoru" 或 "test"
        For j = 1 To lastCol
            If InStr(1, ws.Cells(i, j).Value, "mojoru", vbTextCompare) > 0 Or _
               InStr(1, ws.Cells(i, j).Value, "test", vbTextCompare) > 0 Then
                rowContainsKeyword = True
                Exit For
            End If
        Next j
        
        ' 如果当前行不包含关键词，则清除整行内容
        If Not rowContainsKeyword Then
            ws.Rows(i).Value = ""
        End If
    Next i
    
    ' 功能 2：遍历每一列
    For j = 1 To lastCol
        For i = 1 To lastRow
            ' 检查当前单元格是否包含 "mojoru"
            If InStr(1, ws.Cells(i, j).Value, "mojoru", vbTextCompare) > 0 Then
                ' 将该单元格下方的单元格设置为当前日期
                ws.Cells(i + 1, j).Value = currentDate
                ws.Cells(i + 1, j).NumberFormat = "yyyy/mm/dd"
            End If
        Next i
    Next j
    
    Exit Sub
    
ErrorHandler:
    MsgBox "错误 " & Err.Number & ": " & Err.Description, vbCritical, "Macro Error"
End Sub

' 辅助函数
Public Function GetVersion() As String
    GetVersion = "Test Macro v1.0"
End Function
