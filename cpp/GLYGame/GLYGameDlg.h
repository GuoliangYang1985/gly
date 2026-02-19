// GLYGameDlg.h : header file
//

#if !defined(AFX_GLYGAMEDLG_H__C2D68685_30D8_4E6D_B7A3_49B9DDEB3446__INCLUDED_)
#define AFX_GLYGAMEDLG_H__C2D68685_30D8_4E6D_B7A3_49B9DDEB3446__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#include <afxtempl.h>
#include "Avatar.h"
#include "BackGround.h"
#include "Item.h"
#include "ItemDefinition.h"
#include "RenderGrid.h"
#include "Astar.h"
#import "msxml4.dll"
using namespace MSXML2;
#endif // _MSC_VER > 1000


/////////////////////////////////////////////////////////////////////////////
// CGLYGameDlg dialog

class CGLYGameDlg : public CDialog, public ISearchable
{
	// Construction
public:
	CGLYGameDlg(CWnd* pParent = NULL);	// standard constructor
	virtual ~CGLYGameDlg();
	// Dialog Data
		//{{AFX_DATA(CGLYGameDlg)
	enum { IDD = IDD_GLYGAME_DIALOG };
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CGLYGameDlg)
protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
public:
	//创建背景。
	void CreateBackGroud();
	//事件处理。
	LRESULT WindowProc(UINT uMsg, WPARAM wParam, LPARAM lParam);
	//鼠标左键按下处理。
	void LButtonDown(UINT modKeys, CPoint point);
	//开始计时器。
	void StartTimer();
	//时间处理。
	void OnTimer(int id);
	//画指定alpha值的矩形。
	void DrawAlphaRect(CDC* pDC, CRect& r, COLORREF clr, unsigned char alpha);
	//刷新游戏画面。
	void GamePaint();
	/**
	 * 画出所有有序元素。
	 */
	void DrawSortedAll();
	void RenderAll();
	/**
	 * 解析所有素材定义数据并创建与之对应的对象。
	 */
	void CreateAllItemDefination();
	/**
	 * 删除ItemDefination。
	 */
	void DeleteAllItemDefination();
	/**
	 * 解析所有素材数据并创建与之对应的对象。
	 */
	void CreateAllItem();
	/**
	 * 加载地图数据。
	 */
	void LoadMapData();
	/**
	 * 得到CString类型的属性值。
	 * @param pXmlMapConfig xml配置文件。
	 * @bstrtNode 节点名。
	 * @bstrtAttribute 属性名。
	 * @return CString类型的属性值。
	 */
	CString GetAttribute(MSXML2::IXMLDOMDocumentPtr pXmlMapConfig, _bstr_t bstrtNode, _bstr_t bstrtAttribute);
	/**
	 * 得到float类型的属性值。
	 * @param pXmlMapConfig xml配置文件。
	 * @bstrtNode 节点名。
	 * @bstrtAttribute 属性名。
	 * @return float类型的属性值。
	 */
	float GetAttributeF(MSXML2::IXMLDOMDocumentPtr pXmlMapConfig, _bstr_t bstrtNode, _bstr_t bstrtAttribute);
	/**
	 * 获取单元格。
	 * @param tx 屏幕的x轴坐标。
	 * @param ty 屏幕的y轴坐标。
	 * @return 得到对应的单元格。
	 */
	CTile* GetTileFromScreenCoordinate(float tx, float ty);
	CTile* GetTile(int col, int row);
	float GetNodeTransitionCost(INode* n1, INode* n2);
	/**
	 * 排序。
	 */
	void SortPosition();

	int GetCols();
	int GetRows();
	INode* GetNode(int col, int row);
public:
	//角色。
	CAvatar m_Avatar;
	//背景。
	CBackGround m_BackGround;
	//是否初始化完成。
	bool m_bIsReady;
	//地图配置信息。
	MSXML2::IXMLDOMDocumentPtr m_pXmlMapConfig;
	//素材存放根路径。
	CString m_strBaseDir;
	Image* m_back;
	//物件实例。
	vector<CItem*>* m_pArrItems;
	//物件定义。
	CMap<CString, LPCTSTR, CItemDefinition*, CItemDefinition*> m_itemDefinitions;
	//网格层。
	CRenderGrid m_renderGrid;
	//游戏所占的列数。
	int m_nCols;
	//游戏所占的行数。
	int m_nRows;
	//用于寻路。
	CAstar m_astar;

	GdiplusStartupInput m_gdiplusStartupInput;
	ULONG_PTR m_pGdiToken;
	//地图和背景。
	CDC mBackDC;
	//地图的所有内容。
	CDC mMapDC;
	bool mBackDone;
	float mMapX;
	float mMapY;
protected:
	HICON m_hIcon;
public:
	// Generated message map functions
	//{{AFX_MSG(CGLYGameDlg)
	virtual BOOL OnInitDialog();
	afx_msg void OnSize(UINT nType, int cx, int cy);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

#endif // !defined(AFX_GLYGAMEDLG_H__C2D68685_30D8_4E6D_B7A3_49B9DDEB3446__INCLUDED_)
