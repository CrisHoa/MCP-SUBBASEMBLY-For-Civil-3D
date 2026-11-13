"""
Tạo cấu kiện GPC_DUONGQL13_Goc_P10 với điểm gốc tại P10.
Khớp 100% hình học, kích thước, vật liệu và mã của GPC_DUONGQL13 - TR v1.pkt.
"""

from pathlib import Path
import shutil
import zipfile
from sac_mcp.core.validator import PktValidator

def generate_xaml_goc_p10() -> str:
    xaml = '''<Activity mc:Ignorable="sads sap" x:Class="Subassembly" this:Subassembly.Side="[new EnumType(-1, &quot;None&quot;, &quot;Side&quot;)]" this:Subassembly.B_bv="0.15" this:Subassembly.H_bv_tren="0.1" this:Subassembly.H_btl="0.06" this:Subassembly.H_bv_duoi="0.1" this:Subassembly.H_vat1="0.02" this:Subassembly.H_vat2="0.18" this:Subassembly.B_vat1="0.02" this:Subassembly.B_vat2="0.03" this:Subassembly.H_DINH="0.05"
 xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
 xmlns:asa="clr-namespace:Autodesk.SubassemblyComposer.API;assembly=Subassembly.API"
 xmlns:asa1="clr-namespace:Autodesk.SubassemblyComposer.ActivityLibrary;assembly=Subassembly.ActivityLibrary"
 xmlns:asw="clr-namespace:Autodesk.SubassemblyComposer.WorkflowEngine;assembly=Subassembly.WorkflowEngine"
 xmlns:av="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
 xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
 xmlns:mva="clr-namespace:Microsoft.VisualBasic.Activities;assembly=System.Activities"
 xmlns:s="clr-namespace:System;assembly=mscorlib"
 xmlns:s1="clr-namespace:System;assembly=System.Core"
 xmlns:s2="clr-namespace:System;assembly=System"
 xmlns:sa="clr-namespace:System.Activities;assembly=System.Activities"
 xmlns:sads="http://schemas.microsoft.com/netfx/2010/xaml/activities/debugger"
 xmlns:sap="http://schemas.microsoft.com/netfx/2009/xaml/activities/presentation"
 xmlns:scg="clr-namespace:System.Collections.Generic;assembly=mscorlib"
 xmlns:this="clr-namespace:"
 xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <x:Members>
    <x:Property Name="Geometry" Type="InOutArgument(asw:Geometry)" />
    <x:Property Name="SubassemblyErrorCenter" Type="InOutArgument(asw:SubassemblyErrorCenter)" />
    <x:Property Name="SubassemblyRunMode" Type="InOutArgument(asw:SubassemblyRunMode)" />
    <x:Property Name="Side" Type="InArgument(asw:EnumType)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="B_bv" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
        <asw:DisplayName2Attribute DisplayName="bề rộng bó nền" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="H_bv_tren" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:DisplayName2Attribute DisplayName="chiều cao bó nền" />
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="H_btl" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
        <asw:DisplayName2Attribute DisplayName="chiều cao btl" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="H_bv_duoi" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="H_vat1" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
        <asw:DisplayName2Attribute DisplayName="chiều cao đoạn vát 1" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="H_vat2" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
        <asw:DisplayName2Attribute DisplayName="chiều cao đoạn vát 2" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="B_vat1" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
        <asw:DisplayName2Attribute DisplayName="chiều rộng đoạn vát 1" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="B_vat2" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
        <asw:DisplayName2Attribute DisplayName="chiều rộng đoạn vát 1" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="H_DINH" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
        <asw:DisplayName2Attribute DisplayName="CHIỀU CAO TỪ LỚP CỎ TỚI ĐỈNH GPC" />
      </x:Property.Attributes>
    </x:Property>
  </x:Members>
  <sap:VirtualizedContainerService.HintSize>654,1050</sap:VirtualizedContainerService.HintSize>
  <mva:VisualBasic.Settings>Assembly references and imported namespaces serialized as XML namespaces</mva:VisualBasic.Settings>
  <Flowchart sap:VirtualizedContainerService.HintSize="614,1010" mva:VisualBasic.Settings="Assembly references and imported namespaces serialized as XML namespaces">
    <Flowchart.Variables>
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(41, &quot;AwayFromCrown&quot;)]" Modifiers="ReadOnly" Name="AwayFromCrown" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(1, &quot;Left&quot;)]" Modifiers="ReadOnly" Name="Left" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(20, &quot;LeftInsideLane&quot;)]" Modifiers="ReadOnly" Name="LeftInsideLane" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(21, &quot;LeftInsideShoulder&quot;)]" Modifiers="ReadOnly" Name="LeftInsideShoulder" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(22, &quot;LeftOutsideLane&quot;)]" Modifiers="ReadOnly" Name="LeftOutsideLane" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(23, &quot;LeftOutsideShoulder&quot;)]" Modifiers="ReadOnly" Name="LeftOutsideShoulder" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(11, &quot;No&quot;)]" Modifiers="ReadOnly" Name="No" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(-1, &quot;None&quot;)]" Modifiers="ReadOnly" Name="None" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(0, &quot;Right&quot;)]" Modifiers="ReadOnly" Name="Right" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(24, &quot;RightInsideLane&quot;)]" Modifiers="ReadOnly" Name="RightInsideLane" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(25, &quot;RightInsideShoulder&quot;)]" Modifiers="ReadOnly" Name="RightInsideShoulder" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(26, &quot;RightOutsideLane&quot;)]" Modifiers="ReadOnly" Name="RightOutsideLane" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(27, &quot;RightOutsideShoulder&quot;)]" Modifiers="ReadOnly" Name="RightOutsideShoulder" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(30, &quot;Supported&quot;)]" Modifiers="ReadOnly" Name="Supported" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(40, &quot;TowardsCrown&quot;)]" Modifiers="ReadOnly" Name="TowardsCrown" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(31, &quot;Unsupported&quot;)]" Modifiers="ReadOnly" Name="Unsupported" />
      <Variable x:TypeArguments="asw:EnumType" Default="[new EnumType(10, &quot;Yes&quot;)]" Modifiers="ReadOnly" Name="Yes" />
    </Flowchart.Variables>
    <sap:WorkflowViewStateService.ViewState>
      <scg:Dictionary x:TypeArguments="x:String, x:Object">
        <x:Boolean x:Key="IsExpanded">False</x:Boolean>
        <av:Point x:Key="ShapeLocation">270,2.5</av:Point>
        <av:Size x:Key="ShapeSize">60,75</av:Size>
        <av:PointCollection x:Key="ConnectorLocation">300,77.5 400,77.5 400,100</av:PointCollection>
        <x:Double x:Key="Height">980</x:Double>
      </scg:Dictionary>
    </sap:WorkflowViewStateService.ViewState>
    <Flowchart.StartNode>
      <FlowStep x:Name="__ReferenceID0">
        <sap:WorkflowViewStateService.ViewState>
          <scg:Dictionary x:TypeArguments="x:String, x:Object">
            <av:Point x:Key="ShapeLocation">200,89</av:Point>
            <av:Size x:Key="ShapeSize">200,22</av:Size>
            <av:PointCollection x:Key="ConnectorLocation">300,111 280,111 280,129</av:PointCollection>
          </scg:Dictionary>
        </sap:WorkflowViewStateService.ViewState>
        <asa1:CreatePoint AutoLinkCodes="{x:Null}" AutoLinkGeometryName="{x:Null}" FromPoint="{x:Null}" ActivityId="1" ApplyAOR="False" AutoLink="False" DisplayName="P10" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P10" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
          <asa1:CreatePoint.Arguments>
            <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">0</InArgument>
            <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">0</InArgument>
          </asa1:CreatePoint.Arguments>
          <asa1:CreatePoint.PointCodes>
            <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
              <InArgument x:TypeArguments="x:String">BN1.P10</InArgument>
            </scg:List>
          </asa1:CreatePoint.PointCodes>
          <sap:WorkflowViewStateService.ViewState>
            <scg:Dictionary x:TypeArguments="x:String, x:Object">
              <x:Boolean x:Key="IsExpanded">True</x:Boolean>
            </scg:Dictionary>
          </sap:WorkflowViewStateService.ViewState>
        </asa1:CreatePoint>
        <FlowStep.Next>
          <FlowStep x:Name="__ReferenceID1">
            <sap:WorkflowViewStateService.ViewState>
              <scg:Dictionary x:TypeArguments="x:String, x:Object">
                <av:Point x:Key="ShapeLocation">180,129</av:Point>
                <av:Size x:Key="ShapeSize">200,22</av:Size>
                <av:PointCollection x:Key="ConnectorLocation">280,151 280,159</av:PointCollection>
              </scg:Dictionary>
            </sap:WorkflowViewStateService.ViewState>
            <asa1:CreatePoint ActivityId="2" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L2" DisplayName="P3&amp;L2" FromPoint="P10" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P3" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
              <asa1:CreatePoint.Arguments>
                <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">0</InArgument>
                <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">[-H_bv_duoi]</InArgument>
              </asa1:CreatePoint.Arguments>
              <asa1:CreatePoint.AutoLinkCodes>
                <scg:List x:TypeArguments="InArgument(x:String)" Capacity="0" />
              </asa1:CreatePoint.AutoLinkCodes>
              <asa1:CreatePoint.PointCodes>
                <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                  <InArgument x:TypeArguments="x:String">BN1.P3</InArgument>
                </scg:List>
              </asa1:CreatePoint.PointCodes>
              <sap:WorkflowViewStateService.ViewState>
                <scg:Dictionary x:TypeArguments="x:String, x:Object">
                  <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                </scg:Dictionary>
              </sap:WorkflowViewStateService.ViewState>
            </asa1:CreatePoint>
            <FlowStep.Next>
              <FlowStep x:Name="__ReferenceID2">
                <sap:WorkflowViewStateService.ViewState>
                  <scg:Dictionary x:TypeArguments="x:String, x:Object">
                    <av:Point x:Key="ShapeLocation">180,159</av:Point>
                    <av:Size x:Key="ShapeSize">200,22</av:Size>
                    <av:PointCollection x:Key="ConnectorLocation">280,181 280,189</av:PointCollection>
                  </scg:Dictionary>
                </sap:WorkflowViewStateService.ViewState>
                <asa1:CreatePoint AutoLinkCodes="{x:Null}" ActivityId="3" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L3" DisplayName="P4&amp;L3" FromPoint="P3" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P4" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                  <asa1:CreatePoint.Arguments>
                    <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">[-(B_bv+B_vat1+B_vat2)]</InArgument>
                    <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">0</InArgument>
                  </asa1:CreatePoint.Arguments>
                  <asa1:CreatePoint.PointCodes>
                    <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                      <InArgument x:TypeArguments="x:String">BN1.P4</InArgument>
                    </scg:List>
                  </asa1:CreatePoint.PointCodes>
                  <sap:WorkflowViewStateService.ViewState>
                    <scg:Dictionary x:TypeArguments="x:String, x:Object">
                      <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                    </scg:Dictionary>
                  </sap:WorkflowViewStateService.ViewState>
                </asa1:CreatePoint>
                <FlowStep.Next>
                  <FlowStep x:Name="__ReferenceID3">
                    <sap:WorkflowViewStateService.ViewState>
                      <scg:Dictionary x:TypeArguments="x:String, x:Object">
                        <av:Point x:Key="ShapeLocation">180,189</av:Point>
                        <av:Size x:Key="ShapeSize">200,22</av:Size>
                        <av:PointCollection x:Key="ConnectorLocation">280,211 280,229</av:PointCollection>
                      </scg:Dictionary>
                    </sap:WorkflowViewStateService.ViewState>
                    <asa1:CreatePoint ActivityId="4" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L4" DisplayName="P1&amp;L4" FromPoint="P4" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P1" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                      <asa1:CreatePoint.Arguments>
                        <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">0</InArgument>
                        <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">[H_bv_duoi]</InArgument>
                      </asa1:CreatePoint.Arguments>
                      <asa1:CreatePoint.AutoLinkCodes>
                        <scg:List x:TypeArguments="InArgument(x:String)" Capacity="0" />
                      </asa1:CreatePoint.AutoLinkCodes>
                      <asa1:CreatePoint.PointCodes>
                        <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                          <InArgument x:TypeArguments="x:String">BN1.P1</InArgument>
                        </scg:List>
                      </asa1:CreatePoint.PointCodes>
                      <sap:WorkflowViewStateService.ViewState>
                        <scg:Dictionary x:TypeArguments="x:String, x:Object">
                          <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                        </scg:Dictionary>
                      </sap:WorkflowViewStateService.ViewState>
                    </asa1:CreatePoint>
                    <FlowStep.Next>
                      <FlowStep x:Name="__ReferenceID4">
                        <sap:WorkflowViewStateService.ViewState>
                          <scg:Dictionary x:TypeArguments="x:String, x:Object">
                            <av:Point x:Key="ShapeLocation">180,229</av:Point>
                            <av:Size x:Key="ShapeSize">200,22</av:Size>
                            <av:PointCollection x:Key="ConnectorLocation">280,251 280,269</av:PointCollection>
                          </scg:Dictionary>
                        </sap:WorkflowViewStateService.ViewState>
                        <asa1:CreatePoint ActivityId="5" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L12" DisplayName="P7&amp;L12" FromPoint="P1" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P7" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                          <asa1:CreatePoint.Arguments>
                            <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">0</InArgument>
                            <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">[H_bv_tren]</InArgument>
                          </asa1:CreatePoint.Arguments>
                          <asa1:CreatePoint.AutoLinkCodes>
                            <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                              <InArgument x:TypeArguments="x:String">Top</InArgument>
                            </scg:List>
                          </asa1:CreatePoint.AutoLinkCodes>
                          <asa1:CreatePoint.PointCodes>
                            <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                              <InArgument x:TypeArguments="x:String">BN1.P4</InArgument>
                            </scg:List>
                          </asa1:CreatePoint.PointCodes>
                          <sap:WorkflowViewStateService.ViewState>
                            <scg:Dictionary x:TypeArguments="x:String, x:Object">
                              <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                            </scg:Dictionary>
                          </sap:WorkflowViewStateService.ViewState>
                        </asa1:CreatePoint>
                        <FlowStep.Next>
                          <FlowStep x:Name="__ReferenceID5">
                            <sap:WorkflowViewStateService.ViewState>
                              <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                <av:Point x:Key="ShapeLocation">180,269</av:Point>
                                <av:Size x:Key="ShapeSize">200,22</av:Size>
                                <av:PointCollection x:Key="ConnectorLocation">280,291 280,309</av:PointCollection>
                              </scg:Dictionary>
                            </sap:WorkflowViewStateService.ViewState>
                            <asa1:CreatePoint ActivityId="6" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L1" DisplayName="P2&amp;L1" FromPoint="P7" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P2" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                              <asa1:CreatePoint.Arguments>
                                <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">[B_vat2]</InArgument>
                                <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">[H_vat2]</InArgument>
                              </asa1:CreatePoint.Arguments>
                              <asa1:CreatePoint.AutoLinkCodes>
                                <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                  <InArgument x:TypeArguments="x:String">Top</InArgument>
                                </scg:List>
                              </asa1:CreatePoint.AutoLinkCodes>
                              <asa1:CreatePoint.PointCodes>
                                <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                  <InArgument x:TypeArguments="x:String">BN1.P2</InArgument>
                                </scg:List>
                              </asa1:CreatePoint.PointCodes>
                              <sap:WorkflowViewStateService.ViewState>
                                <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                  <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                                </scg:Dictionary>
                              </sap:WorkflowViewStateService.ViewState>
                            </asa1:CreatePoint>
                            <FlowStep.Next>
                              <FlowStep x:Name="__ReferenceID6">
                                <sap:WorkflowViewStateService.ViewState>
                                  <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                    <av:Point x:Key="ShapeLocation">180,309</av:Point>
                                    <av:Size x:Key="ShapeSize">200,22</av:Size>
                                    <av:PointCollection x:Key="ConnectorLocation">280,331 280,349</av:PointCollection>
                                  </scg:Dictionary>
                                </sap:WorkflowViewStateService.ViewState>
                                <asa1:CreatePoint ActivityId="7" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L9" DisplayName="P8&amp;L9" FromPoint="P2" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P8" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                                  <asa1:CreatePoint.Arguments>
                                    <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">[B_vat1]</InArgument>
                                    <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">[H_vat1]</InArgument>
                                  </asa1:CreatePoint.Arguments>
                                  <asa1:CreatePoint.AutoLinkCodes>
                                    <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                      <InArgument x:TypeArguments="x:String">Top</InArgument>
                                    </scg:List>
                                  </asa1:CreatePoint.AutoLinkCodes>
                                  <asa1:CreatePoint.PointCodes>
                                    <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                      <InArgument x:TypeArguments="x:String">BN1.P4</InArgument>
                                    </scg:List>
                                  </asa1:CreatePoint.PointCodes>
                                  <sap:WorkflowViewStateService.ViewState>
                                    <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                      <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                                    </scg:Dictionary>
                                  </sap:WorkflowViewStateService.ViewState>
                                </asa1:CreatePoint>
                                <FlowStep.Next>
                                  <FlowStep x:Name="__ReferenceID7">
                                    <sap:WorkflowViewStateService.ViewState>
                                      <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                        <av:Point x:Key="ShapeLocation">180,349</av:Point>
                                        <av:Size x:Key="ShapeSize">200,22</av:Size>
                                        <av:PointCollection x:Key="ConnectorLocation">280,371 280,389</av:PointCollection>
                                      </scg:Dictionary>
                                    </sap:WorkflowViewStateService.ViewState>
                                    <asa1:CreatePoint ActivityId="8" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L10" DisplayName="P9&amp;L10" FromPoint="P8" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P9" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                                      <asa1:CreatePoint.Arguments>
                                        <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">[B_bv]</InArgument>
                                        <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">0</InArgument>
                                      </asa1:CreatePoint.Arguments>
                                      <asa1:CreatePoint.AutoLinkCodes>
                                        <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                          <InArgument x:TypeArguments="x:String">Top</InArgument>
                                        </scg:List>
                                      </asa1:CreatePoint.AutoLinkCodes>
                                      <asa1:CreatePoint.PointCodes>
                                        <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                          <InArgument x:TypeArguments="x:String">BN1.P9</InArgument>
                                        </scg:List>
                                      </asa1:CreatePoint.PointCodes>
                                      <sap:WorkflowViewStateService.ViewState>
                                        <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                          <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                                        </scg:Dictionary>
                                      </sap:WorkflowViewStateService.ViewState>
                                    </asa1:CreatePoint>
                                    <FlowStep.Next>
                                      <FlowStep x:Name="__ReferenceID8">
                                        <sap:WorkflowViewStateService.ViewState>
                                          <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                            <av:Point x:Key="ShapeLocation">180,389</av:Point>
                                            <av:Size x:Key="ShapeSize">200,22</av:Size>
                                            <av:PointCollection x:Key="ConnectorLocation">280,411 280,439</av:PointCollection>
                                          </scg:Dictionary>
                                        </sap:WorkflowViewStateService.ViewState>
                                        <asa1:CreateLink ActivityId="9" ApplyAOR="False" DisplayName="L11" EndPoint="P10" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" IsEnabled="True" LinkNumber="L11" ShowErrors="True" StartPoint="P9" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                                          <asa1:CreateLink.LinkCodes>
                                            <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                              <InArgument x:TypeArguments="x:String">Top</InArgument>
                                            </scg:List>
                                          </asa1:CreateLink.LinkCodes>
                                          <sap:WorkflowViewStateService.ViewState>
                                            <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                              <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                                            </scg:Dictionary>
                                          </sap:WorkflowViewStateService.ViewState>
                                        </asa1:CreateLink>
                                        <FlowStep.Next>
                                          <FlowStep x:Name="__ReferenceID9">
                                            <sap:WorkflowViewStateService.ViewState>
                                              <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                <av:Point x:Key="ShapeLocation">180,439</av:Point>
                                                <av:Size x:Key="ShapeSize">200,22</av:Size>
                                                <av:PointCollection x:Key="ConnectorLocation">280,461 280,489</av:PointCollection>
                                              </scg:Dictionary>
                                            </sap:WorkflowViewStateService.ViewState>
                                            <asa1:CreateShape ActivityId="10" DisplayName="S1" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" Links="L1,L4,L3,L2,L11,L10,L9,L12" ShapeNumber="S1" ShowErrors="True" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                                              <asa1:CreateShape.ComponentNames>
                                                <x:String>L1</x:String>
                                                <x:String>L4</x:String>
                                                <x:String>L3</x:String>
                                                <x:String>L2</x:String>
                                                <x:String>L11</x:String>
                                                <x:String>L10</x:String>
                                                <x:String>L9</x:String>
                                                <x:String>L12</x:String>
                                              </asa1:CreateShape.ComponentNames>
                                              <asa1:CreateShape.ShapeCodes>
                                                <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                                  <InArgument x:TypeArguments="x:String">BN1.M250</InArgument>
                                                </scg:List>
                                              </asa1:CreateShape.ShapeCodes>
                                              <sap:WorkflowViewStateService.ViewState>
                                                <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                  <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                                                </scg:Dictionary>
                                              </sap:WorkflowViewStateService.ViewState>
                                            </asa1:CreateShape>
                                            <FlowStep.Next>
                                              <FlowStep x:Name="__ReferenceID10">
                                                <sap:WorkflowViewStateService.ViewState>
                                                  <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                    <av:Point x:Key="ShapeLocation">180,489</av:Point>
                                                    <av:Size x:Key="ShapeSize">200,22</av:Size>
                                                    <av:PointCollection x:Key="ConnectorLocation">280,511 280,539</av:PointCollection>
                                                  </scg:Dictionary>
                                                </sap:WorkflowViewStateService.ViewState>
                                                <asa1:CreatePoint ActivityId="11" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L5" DisplayName="P5&amp;L5" FromPoint="P4" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P5" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                                                  <asa1:CreatePoint.Arguments>
                                                    <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">0</InArgument>
                                                    <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">[-H_btl]</InArgument>
                                                  </asa1:CreatePoint.Arguments>
                                                  <asa1:CreatePoint.AutoLinkCodes>
                                                    <scg:List x:TypeArguments="InArgument(x:String)" Capacity="0" />
                                                  </asa1:CreatePoint.AutoLinkCodes>
                                                  <asa1:CreatePoint.PointCodes>
                                                    <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                                      <InArgument x:TypeArguments="x:String">BN1.P5</InArgument>
                                                    </scg:List>
                                                  </asa1:CreatePoint.PointCodes>
                                                  <sap:WorkflowViewStateService.ViewState>
                                                    <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                      <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                                                    </scg:Dictionary>
                                                  </sap:WorkflowViewStateService.ViewState>
                                                </asa1:CreatePoint>
                                                <FlowStep.Next>
                                                  <FlowStep x:Name="__ReferenceID11">
                                                    <sap:WorkflowViewStateService.ViewState>
                                                      <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                        <av:Point x:Key="ShapeLocation">180,539</av:Point>
                                                        <av:Size x:Key="ShapeSize">200,22</av:Size>
                                                        <av:PointCollection x:Key="ConnectorLocation">280,561 280,589</av:PointCollection>
                                                      </scg:Dictionary>
                                                    </sap:WorkflowViewStateService.ViewState>
                                                    <asa1:CreatePoint ActivityId="12" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L6" DisplayName="P6&amp;L6" FromPoint="P5" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P6" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                                                      <asa1:CreatePoint.Arguments>
                                                        <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">[(B_bv+B_vat1+B_vat2)]</InArgument>
                                                        <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">0</InArgument>
                                                      </asa1:CreatePoint.Arguments>
                                                      <asa1:CreatePoint.AutoLinkCodes>
                                                        <scg:List x:TypeArguments="InArgument(x:String)" Capacity="0" />
                                                      </asa1:CreatePoint.AutoLinkCodes>
                                                      <asa1:CreatePoint.PointCodes>
                                                        <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                                          <InArgument x:TypeArguments="x:String">BN1.P6</InArgument>
                                                        </scg:List>
                                                      </asa1:CreatePoint.PointCodes>
                                                      <sap:WorkflowViewStateService.ViewState>
                                                        <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                          <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                                                        </scg:Dictionary>
                                                      </sap:WorkflowViewStateService.ViewState>
                                                    </asa1:CreatePoint>
                                                    <FlowStep.Next>
                                                      <FlowStep x:Name="__ReferenceID12">
                                                        <sap:WorkflowViewStateService.ViewState>
                                                          <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                            <av:Point x:Key="ShapeLocation">180,589</av:Point>
                                                            <av:Size x:Key="ShapeSize">200,22</av:Size>
                                                            <av:PointCollection x:Key="ConnectorLocation">280,611 280,639</av:PointCollection>
                                                          </scg:Dictionary>
                                                        </sap:WorkflowViewStateService.ViewState>
                                                        <asa1:CreateLink ActivityId="13" ApplyAOR="False" DisplayName="L7" EndPoint="P6" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" IsEnabled="True" LinkNumber="L7" ShowErrors="True" StartPoint="P3" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                                                          <asa1:CreateLink.LinkCodes>
                                                            <scg:List x:TypeArguments="InArgument(x:String)" Capacity="0" />
                                                          </asa1:CreateLink.LinkCodes>
                                                          <sap:WorkflowViewStateService.ViewState>
                                                            <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                              <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                                                            </scg:Dictionary>
                                                          </sap:WorkflowViewStateService.ViewState>
                                                        </asa1:CreateLink>
                                                        <FlowStep.Next>
                                                          <FlowStep x:Name="__ReferenceID13">
                                                            <sap:WorkflowViewStateService.ViewState>
                                                              <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                                <av:Point x:Key="ShapeLocation">180,639</av:Point>
                                                                <av:Size x:Key="ShapeSize">200,22</av:Size>
                                                              </scg:Dictionary>
                                                            </sap:WorkflowViewStateService.ViewState>
                                                            <asa1:CreateShape ActivityId="14" DisplayName="S2" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" Links="L3,L5,L6,L7" ShapeNumber="S2" ShowErrors="True" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                                                              <asa1:CreateShape.ComponentNames>
                                                                <x:String>L3</x:String>
                                                                <x:String>L5</x:String>
                                                                <x:String>L6</x:String>
                                                                <x:String>L7</x:String>
                                                              </asa1:CreateShape.ComponentNames>
                                                              <asa1:CreateShape.ShapeCodes>
                                                                <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                                                  <InArgument x:TypeArguments="x:String">BN1.M150</InArgument>
                                                                </scg:List>
                                                              </asa1:CreateShape.ShapeCodes>
                                                              <sap:WorkflowViewStateService.ViewState>
                                                                <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                                  <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                                                                </scg:Dictionary>
                                                              </sap:WorkflowViewStateService.ViewState>
                                                            </asa1:CreateShape>
                                                          </FlowStep>
                                                        </FlowStep.Next>
                                                      </FlowStep>
                                                    </FlowStep.Next>
                                                  </FlowStep>
                                                </FlowStep.Next>
                                              </FlowStep>
                                            </FlowStep.Next>
                                          </FlowStep>
                                        </FlowStep.Next>
                                      </FlowStep>
                                    </FlowStep.Next>
                                  </FlowStep>
                                </FlowStep.Next>
                              </FlowStep>
                            </FlowStep.Next>
                          </FlowStep>
                        </FlowStep.Next>
                      </FlowStep>
                    </FlowStep.Next>
                  </FlowStep>
                </FlowStep.Next>
              </FlowStep>
            </FlowStep.Next>
          </FlowStep>
        </FlowStep.Next>
      </FlowStep>
    </Flowchart.StartNode>
    <x:Reference>__ReferenceID0</x:Reference>
    <x:Reference>__ReferenceID1</x:Reference>
    <x:Reference>__ReferenceID2</x:Reference>
    <x:Reference>__ReferenceID3</x:Reference>
    <x:Reference>__ReferenceID4</x:Reference>
    <x:Reference>__ReferenceID5</x:Reference>
    <x:Reference>__ReferenceID6</x:Reference>
    <x:Reference>__ReferenceID7</x:Reference>
    <x:Reference>__ReferenceID8</x:Reference>
    <x:Reference>__ReferenceID9</x:Reference>
    <x:Reference>__ReferenceID10</x:Reference>
    <x:Reference>__ReferenceID11</x:Reference>
    <x:Reference>__ReferenceID12</x:Reference>
    <x:Reference>__ReferenceID13</x:Reference>
  </Flowchart>
</Activity>'''
    return xaml

def build_pkt(output_pkt: Path):
    src_dir = Path(r'C:\Users\Admin\AppData\Local\Temp\C3DSA\GPC_DUONGQL13 - TR v1.pkt.01a3ebcd03934d56919f0b2a24abd9ee')
    guid = 'be9d9d838b3a4120933f22853bda2ef5'
    
    # Chuẩn bị nội dung
    atc_bytes = (src_dir / f'{guid}.atc').read_bytes()
    cfg_bytes = (src_dir / f'{guid}.cfg').read_bytes()
    pvd_bytes = (src_dir / f'{guid}.pvd').read_bytes()
    emd_bytes = (src_dir / f'{guid}.emd').read_bytes()
    cdmd_bytes = (src_dir / f'{guid}.cdmd').read_bytes()
    png_bytes = (src_dir / 'GPC.png').read_bytes()
    
    # XAML mới với UTF-8 BOM
    new_xaml = generate_xaml_goc_p10()
    xaml_bytes = '\ufeff'.encode('utf-8') + new_xaml.encode('utf-8')
    
    # Đóng gói zip OPC
    content_types = '''<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="atc" ContentType="application/vnd.autodesk.c3d.sac.atc+xml" />
  <Default Extension="cfg" ContentType="application/vnd.autodesk.c3d.sac.cfg+xml" />
  <Default Extension="xaml" ContentType="application/vnd.autodesk.c3d.sac.xaml+xml" />
  <Default Extension="pvd" ContentType="application/vnd.autodesk.c3d.sac.pvd+xml" />
  <Default Extension="emd" ContentType="application/vnd.autodesk.c3d.sac.emd+xml" />
  <Default Extension="cdmd" ContentType="application/vnd.autodesk.c3d.sac.cdmd+xml" />
  <Default Extension="png" ContentType="image/png" />
</Types>'''

    output_pkt.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_pkt, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types.encode('utf-8'))
        zf.writestr(f'{guid}.atc', atc_bytes)
        zf.writestr(f'{guid}.cfg', cfg_bytes)
        zf.writestr(f'{guid}.pvd', pvd_bytes)
        zf.writestr(f'{guid}.emd', emd_bytes)
        zf.writestr(f'{guid}.cdmd', cdmd_bytes)
        zf.writestr(f'{guid}.xaml', xaml_bytes)
        zf.writestr('GPC.png', png_bytes)

    print(f'PKT written to {output_pkt}')

if __name__ == '__main__':
    dest = Path('examples/Sub Assembly/Bo_7_Subassembly_Chuan/10_GPC_DUONGQL13_Goc_P10/GPC_DUONGQL13_Goc_P10.pkt')
    build_pkt(dest)
    
    # Copy to Desktop
    desktop_dest = Path(r'C:\Users\Admin\Desktop\GPC_DUONGQL13_Goc_P10.pkt')
    shutil.copy2(dest, desktop_dest)
    print(f'Copied to Desktop: {desktop_dest}')

    # Validate
    rep = PktValidator.validate_pkt(dest, run_native_test=True)
    print('Validation Result:')
    print('  is_valid:', rep.is_valid)
    print('  tier1_opc_ok:', rep.tier1_opc_ok)
    print('  tier2_xaml_ok:', rep.tier2_xaml_ok)
    print('  tier3_native_ok:', rep.tier3_native_ok)
    for issue in rep.issues:
        print(f'  [{issue.severity}] {issue.category}: {issue.message}')
