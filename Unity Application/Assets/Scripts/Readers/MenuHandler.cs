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

    private readonly string[] modeNames = { "Calibrate", "Single Transform", "Free Transform", "Spawn" };

    private void Awake()
    {
        menu = GetComponent<InfiniteScrollHandler>();
    }

    public override void SetDefault()
    {
        mode = 0;
        modeTextField.text = modeNames[0];

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
        else if (instructionValue.StartsWith("Selected"))
        {
            mode = int.Parse(instructionValue.Split(":")[1]);
            modeTextField.text = modeNames[mode];

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