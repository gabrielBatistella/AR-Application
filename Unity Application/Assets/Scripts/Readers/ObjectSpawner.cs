using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;
using UnityEngine.Networking;

public class ObjectSpawner : MonoBehaviour //InstructionReader
{
    [SerializeField] private Transform freeParent;

    public void LoadObject(string hexString, string bundleName)
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

        if (bundle != null)
        {
            GameObject obj = Instantiate(bundle.LoadAsset<GameObject>(bundleName), transform.position, transform.rotation, freeParent);
            bundle.Unload(false);
        }
    }
}