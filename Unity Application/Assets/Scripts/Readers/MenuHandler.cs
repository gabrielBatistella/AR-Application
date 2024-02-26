using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(InfiniteScrollHandler))]
public class MenuHandler : InstructionReader
{
    [SerializeField] private Text modeTextField;

    private InfiniteScrollHandler menu;

    private int mode;
    public int Mode { get => mode; }

    private void Awake()
    {
        menu = GetComponent<InfiniteScrollHandler>();
    }

    public override void SetDefault()
    {
        mode = 0;
        modeTextField.text = "Calibrate";

        menu.SetScrollPosition(0);
        gameObject.SetActive(false);
    }

    public override void FollowInstruction(string instructionValue)
    {
        if (instructionValue == "Close Menu")
        {
            menu.SetScrollPosition(mode);
            gameObject.SetActive(false);
        }
        else if (instructionValue.Contains("Selected"))
        {
            mode = int.Parse(instructionValue.Split(" ")[1]);
            switch (mode)
            {
                case 0:
                {
                    modeTextField.text = "Calibrate";
                    break;
                }
                case 1:
                {
                    modeTextField.text = "Transform";
                    break;
                }
                case 2:
                {
                    modeTextField.text = "Spawn";
                    break;
                }
                default:
                {
                    Debug.Log("Erro no modo do menu");
                    break;
                }
            }
            menu.SetScrollPosition(mode);
            gameObject.SetActive(false);
        }
        else
        {
            if (!gameObject.activeSelf)
            {
                gameObject.SetActive(true);
            }

            string[] scrollInfo = instructionValue.Split(";");
            float scrollPos = int.Parse(scrollInfo[0]) + float.Parse(scrollInfo[1], CultureInfo.InvariantCulture.NumberFormat) / 100f;

            menu.SetScrollPosition(scrollPos);
        }
    }
}
