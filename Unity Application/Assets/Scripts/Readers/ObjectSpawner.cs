using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;

public class ObjectSpawner : InstructionReader
{
    [SerializeField] private Transform objParent;
    [SerializeField] private LayerMask objLayer;

    public override void SetDefault()
    {
        gameObject.SetActive(false);
    }

    public override void FollowInstruction(string instructionValue)
    {
        if (instructionValue.StartsWith("Loading"))
        {
            if (!gameObject.activeSelf)
            {
                gameObject.SetActive(true);
            }

            transform.localPosition = pointFromCoords(instructionValue.Split(" ")[1].Split(";"));
        }
        else
        {
            string[] instructionInfos = instructionValue.Split("/");

            transform.localPosition = pointFromCoords(instructionInfos[0].Split(";"));

            AssetBundle bundle = LoadBundleFromHex(instructionInfos[2]);
            if (bundle != null)
            {
                GameObject obj = Instantiate(bundle.LoadAsset<GameObject>(instructionInfos[1]), transform.position, transform.rotation);
                obj.transform.SetParent(objParent);
                obj.layer = (int) Mathf.Log(objLayer.value, 2);
                bundle.Unload(false);
            }
        }
    }

    private AssetBundle LoadBundleFromHex(string hexString)
    {
        /*
        string bundleURL = bundleFolder + "/" + bundleName + "-";
        #if UNITY_ANDROID
            bundleURL += "Android";
        #else
            bundleURL += "Windows";
        #endif
        AssetBundle bundle = AssetBundle.LoadFromFile(bundleURL);
        */

        if (hexString.Length % 2 != 0)
        {
            throw new ArgumentException("The binary key cannot have an odd number of digits");
        }

        byte[] fileData = new byte[hexString.Length / 2];
        for (int i = 0; i < fileData.Length; i++)
        {
            string byteValue = hexString.Substring(i * 2, 2);
            fileData[i] = byte.Parse(byteValue, NumberStyles.HexNumber, CultureInfo.InvariantCulture);
        }
        AssetBundle bundle = AssetBundle.LoadFromMemory(fileData);

        return bundle;
    }
}