"""
Tạo cấu kiện BV_QL13-TRAI_Goc_P4 với điểm gốc tại P4.
Khớp 100% hình học, kích thước, vật liệu và mã của BV_QL13-TRAI.pkt.
"""

from pathlib import Path
import shutil
import zipfile
from sac_mcp.core.validator import PktValidator


def generate_xaml_bv_trai_goc_p4() -> str:
    xaml = '''<Activity mc:Ignorable="sads sap" x:Class="Subassembly" this:Subassembly.Side="[new EnumType(-1, &quot;None&quot;, &quot;Side&quot;)]" this:Subassembly.H_TREN="0.03" this:Subassembly.H_DUOI="0.14" this:Subassembly.H_XIEN="0.12" this:Subassembly.H_BTL="0.06" this:Subassembly.B_TR="0.05" this:Subassembly.B_PH="0.3" this:Subassembly.B_RV="0.25"
 xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
 xmlns:asa="clr-namespace:Autodesk.SubassemblyComposer.API;assembly=Subassembly.API"
 xmlns:asa1="clr-namespace:Autodesk.SubassemblyComposer.ActivityLibrary;assembly=Subassembly.ActivityLibrary"
 xmlns:asw="clr-namespace:Autodesk.SubassemblyComposer.WorkflowEngine;assembly=Subassembly.WorkflowEngine"
 xmlns:av="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
 xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
 xmlns:mva="clr-namespace:Microsoft.VisualBasic.Activities;assembly=System.Activities"
 xmlns:s="clr-namespace:System;assembly=mscorlib"
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
    <x:Property Name="H_TREN" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="H_DUOI" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="H_XIEN" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="H_BTL" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="B_TR" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="B_PH" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
      </x:Property.Attributes>
    </x:Property>
    <x:Property Name="B_RV" Type="InArgument(x:Double)">
      <x:Property.Attributes>
        <asw:EnabledFlag2Attribute EnabledFlag="True" />
      </x:Property.Attributes>
    </x:Property>
  </x:Members>
  <sap:VirtualizedContainerService.HintSize>755,1657</sap:VirtualizedContainerService.HintSize>
  <mva:VisualBasic.Settings>Assembly references and imported namespaces serialized as XML namespaces</mva:VisualBasic.Settings>
  <Flowchart sap:VirtualizedContainerService.HintSize="715,1617" mva:VisualBasic.Settings="Assembly references and imported namespaces serialized as XML namespaces">
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
        <av:PointCollection x:Key="ConnectorLocation">300,77.5 300,89</av:PointCollection>
        <x:Double x:Key="Height">1580.7142857142858</x:Double>
        <x:Double x:Key="Width">701.088235294118</x:Double>
      </scg:Dictionary>
    </sap:WorkflowViewStateService.ViewState>
    <Flowchart.StartNode>
      <FlowStep x:Name="__ReferenceID0">
        <sap:WorkflowViewStateService.ViewState>
          <scg:Dictionary x:TypeArguments="x:String, x:Object">
            <av:Point x:Key="ShapeLocation">200,89</av:Point>
            <av:Size x:Key="ShapeSize">200,22</av:Size>
            <av:PointCollection x:Key="ConnectorLocation">300,111 300,139</av:PointCollection>
          </scg:Dictionary>
        </sap:WorkflowViewStateService.ViewState>
        <asa1:CreatePoint AutoLinkCodes="{x:Null}" AutoLinkGeometryName="{x:Null}" FromPoint="{x:Null}" ActivityId="1" ApplyAOR="False" AutoLink="False" DisplayName="P4" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P4" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
          <asa1:CreatePoint.Arguments>
            <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">0</InArgument>
            <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">0</InArgument>
          </asa1:CreatePoint.Arguments>
          <asa1:CreatePoint.PointCodes>
            <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
              <InArgument x:TypeArguments="x:String">BV.4</InArgument>
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
                <av:Point x:Key="ShapeLocation">200,139</av:Point>
                <av:Size x:Key="ShapeSize">200,22</av:Size>
                <av:PointCollection x:Key="ConnectorLocation">300,161 300,189</av:PointCollection>
              </scg:Dictionary>
            </sap:WorkflowViewStateService.ViewState>
            <asa1:CreatePoint AutoLinkCodes="{x:Null}" ActivityId="2" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L4" DisplayName="P5&amp;L4" FromPoint="P4" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P5" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
              <asa1:CreatePoint.Arguments>
                <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">0</InArgument>
                <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">[-(H_TREN+H_DUOI+H_XIEN)]</InArgument>
              </asa1:CreatePoint.Arguments>
              <asa1:CreatePoint.PointCodes>
                <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                  <InArgument x:TypeArguments="x:String">BV.5</InArgument>
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
                    <av:Point x:Key="ShapeLocation">200,189</av:Point>
                    <av:Size x:Key="ShapeSize">200,22</av:Size>
                    <av:PointCollection x:Key="ConnectorLocation">300,211 300,239</av:PointCollection>
                  </scg:Dictionary>
                </sap:WorkflowViewStateService.ViewState>
                <asa1:CreatePoint ActivityId="3" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L5" DisplayName="P6&amp;L5" FromPoint="P5" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P6" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                  <asa1:CreatePoint.Arguments>
                    <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">[B_TR+B_PH+B_RV]</InArgument>
                    <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">0</InArgument>
                  </asa1:CreatePoint.Arguments>
                  <asa1:CreatePoint.AutoLinkCodes>
                    <scg:List x:TypeArguments="InArgument(x:String)" Capacity="0" />
                  </asa1:CreatePoint.AutoLinkCodes>
                  <asa1:CreatePoint.PointCodes>
                    <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                      <InArgument x:TypeArguments="x:String">BV.6</InArgument>
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
                        <av:Point x:Key="ShapeLocation">200,239</av:Point>
                        <av:Size x:Key="ShapeSize">200,22</av:Size>
                        <av:PointCollection x:Key="ConnectorLocation">300,261 300,289</av:PointCollection>
                      </scg:Dictionary>
                    </sap:WorkflowViewStateService.ViewState>
                    <asa1:CreatePoint ActivityId="4" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L6" DisplayName="P1&amp;L6" FromPoint="P6" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P1" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                      <asa1:CreatePoint.Arguments>
                        <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">0</InArgument>
                        <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">[H_DUOI+0.01]</InArgument>
                      </asa1:CreatePoint.Arguments>
                      <asa1:CreatePoint.AutoLinkCodes>
                        <scg:List x:TypeArguments="InArgument(x:String)" Capacity="0" />
                      </asa1:CreatePoint.AutoLinkCodes>
                      <asa1:CreatePoint.PointCodes>
                        <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                          <InArgument x:TypeArguments="x:String">BV.1</InArgument>
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
                            <av:Point x:Key="ShapeLocation">200,289</av:Point>
                            <av:Size x:Key="ShapeSize">200,22</av:Size>
                            <av:PointCollection x:Key="ConnectorLocation">300,311 300,339</av:PointCollection>
                          </scg:Dictionary>
                        </sap:WorkflowViewStateService.ViewState>
                        <asa1:CreatePoint ActivityId="5" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L10" DisplayName="P9&amp;L10" FromPoint="P1" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P9" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                          <asa1:CreatePoint.Arguments>
                            <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">[-B_RV]</InArgument>
                            <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">-0.01</InArgument>
                          </asa1:CreatePoint.Arguments>
                          <asa1:CreatePoint.AutoLinkCodes>
                            <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                              <InArgument x:TypeArguments="x:String">Top</InArgument>
                            </scg:List>
                          </asa1:CreatePoint.AutoLinkCodes>
                          <asa1:CreatePoint.PointCodes>
                            <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                              <InArgument x:TypeArguments="x:String">BV.9</InArgument>
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
                                <av:Point x:Key="ShapeLocation">200,339</av:Point>
                                <av:Size x:Key="ShapeSize">200,22</av:Size>
                                <av:PointCollection x:Key="ConnectorLocation">300,361 300,389</av:PointCollection>
                              </scg:Dictionary>
                            </sap:WorkflowViewStateService.ViewState>
                            <asa1:CreatePoint ActivityId="6" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L1" DisplayName="P2&amp;L1" FromPoint="P9" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P2" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                              <asa1:CreatePoint.Arguments>
                                <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">0</InArgument>
                                <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">[H_TREN]</InArgument>
                              </asa1:CreatePoint.Arguments>
                              <asa1:CreatePoint.AutoLinkCodes>
                                <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                  <InArgument x:TypeArguments="x:String">Top</InArgument>
                                </scg:List>
                              </asa1:CreatePoint.AutoLinkCodes>
                              <asa1:CreatePoint.PointCodes>
                                <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                  <InArgument x:TypeArguments="x:String">BV.2</InArgument>
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
                                    <av:Point x:Key="ShapeLocation">200,389</av:Point>
                                    <av:Size x:Key="ShapeSize">200,22</av:Size>
                                    <av:PointCollection x:Key="ConnectorLocation">300,411 300,439</av:PointCollection>
                                  </scg:Dictionary>
                                </sap:WorkflowViewStateService.ViewState>
                                <asa1:CreatePoint ActivityId="7" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L2" DisplayName="P3&amp;L2" FromPoint="P2" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P3" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                                  <asa1:CreatePoint.Arguments>
                                    <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">[-B_PH]</InArgument>
                                    <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">[H_XIEN]</InArgument>
                                  </asa1:CreatePoint.Arguments>
                                  <asa1:CreatePoint.AutoLinkCodes>
                                    <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                      <InArgument x:TypeArguments="x:String">Top</InArgument>
                                    </scg:List>
                                  </asa1:CreatePoint.AutoLinkCodes>
                                  <asa1:CreatePoint.PointCodes>
                                    <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                      <InArgument x:TypeArguments="x:String">BV.3</InArgument>
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
                                        <av:Point x:Key="ShapeLocation">200,439</av:Point>
                                        <av:Size x:Key="ShapeSize">200,22</av:Size>
                                        <av:PointCollection x:Key="ConnectorLocation">300,461 300,489</av:PointCollection>
                                      </scg:Dictionary>
                                    </sap:WorkflowViewStateService.ViewState>
                                    <asa1:CreateLink ActivityId="8" ApplyAOR="False" DisplayName="L3" EndPoint="P4" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" IsEnabled="True" LinkNumber="L3" ShowErrors="True" StartPoint="P3" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
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
                                      <FlowStep x:Name="__ReferenceID8">
                                        <sap:WorkflowViewStateService.ViewState>
                                          <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                            <av:Point x:Key="ShapeLocation">200,489</av:Point>
                                            <av:Size x:Key="ShapeSize">200,22</av:Size>
                                            <av:PointCollection x:Key="ConnectorLocation">300,511 300,539</av:PointCollection>
                                          </scg:Dictionary>
                                        </sap:WorkflowViewStateService.ViewState>
                                        <asa1:CreatePoint ActivityId="9" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L7" DisplayName="P7&amp;L7" FromPoint="P6" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P7" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                                          <asa1:CreatePoint.Arguments>
                                            <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">0</InArgument>
                                            <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">[-H_BTL]</InArgument>
                                          </asa1:CreatePoint.Arguments>
                                          <asa1:CreatePoint.AutoLinkCodes>
                                            <scg:List x:TypeArguments="InArgument(x:String)" Capacity="0" />
                                          </asa1:CreatePoint.AutoLinkCodes>
                                          <asa1:CreatePoint.PointCodes>
                                            <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                              <InArgument x:TypeArguments="x:String">BV.7</InArgument>
                                            </scg:List>
                                          </asa1:CreatePoint.PointCodes>
                                          <sap:WorkflowViewStateService.ViewState>
                                            <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                              <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                                            </scg:Dictionary>
                                          </sap:WorkflowViewStateService.ViewState>
                                        </asa1:CreatePoint>
                                        <FlowStep.Next>
                                          <FlowStep x:Name="__ReferenceID9">
                                            <sap:WorkflowViewStateService.ViewState>
                                              <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                <av:Point x:Key="ShapeLocation">200,539</av:Point>
                                                <av:Size x:Key="ShapeSize">200,22</av:Size>
                                                <av:PointCollection x:Key="ConnectorLocation">300,561 300,589</av:PointCollection>
                                              </scg:Dictionary>
                                            </sap:WorkflowViewStateService.ViewState>
                                            <asa1:CreatePoint ActivityId="10" ApplyAOR="False" AutoLink="True" AutoLinkGeometryName="L8" DisplayName="P8&amp;L8" FromPoint="P5" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" PointNumber="P8" Positioning="DeltaXAndDeltaY" ShowErrors="True" Side="[Side]" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                                              <asa1:CreatePoint.Arguments>
                                                <InArgument x:TypeArguments="x:Double" x:Key="DeltaX1">0</InArgument>
                                                <InArgument x:TypeArguments="x:Double" x:Key="DeltaY1">[-H_BTL]</InArgument>
                                              </asa1:CreatePoint.Arguments>
                                              <asa1:CreatePoint.AutoLinkCodes>
                                                <scg:List x:TypeArguments="InArgument(x:String)" Capacity="0" />
                                              </asa1:CreatePoint.AutoLinkCodes>
                                              <asa1:CreatePoint.PointCodes>
                                                <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                                  <InArgument x:TypeArguments="x:String">BV.8</InArgument>
                                                </scg:List>
                                              </asa1:CreatePoint.PointCodes>
                                              <sap:WorkflowViewStateService.ViewState>
                                                <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                  <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                                                </scg:Dictionary>
                                              </sap:WorkflowViewStateService.ViewState>
                                            </asa1:CreatePoint>
                                            <FlowStep.Next>
                                              <FlowStep x:Name="__ReferenceID10">
                                                <sap:WorkflowViewStateService.ViewState>
                                                  <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                    <av:Point x:Key="ShapeLocation">200,589</av:Point>
                                                    <av:Size x:Key="ShapeSize">200,22</av:Size>
                                                    <av:PointCollection x:Key="ConnectorLocation">300,611 300,639</av:PointCollection>
                                                  </scg:Dictionary>
                                                </sap:WorkflowViewStateService.ViewState>
                                                <asa1:CreateLink ActivityId="11" ApplyAOR="False" DisplayName="L9" EndPoint="P8" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" IsEnabled="True" LinkNumber="L9" ShowErrors="True" StartPoint="P7" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
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
                                                  <FlowStep x:Name="__ReferenceID11">
                                                    <sap:WorkflowViewStateService.ViewState>
                                                      <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                        <av:Point x:Key="ShapeLocation">200,639</av:Point>
                                                        <av:Size x:Key="ShapeSize">200,22</av:Size>
                                                        <av:PointCollection x:Key="ConnectorLocation">300,661 300,689</av:PointCollection>
                                                      </scg:Dictionary>
                                                    </sap:WorkflowViewStateService.ViewState>
                                                    <asa1:CreateShape ActivityId="12" DisplayName="S1" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" Links="L1,L2,L3,L4,L5,L6,L10" ShapeNumber="S1" ShowErrors="True" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                                                      <asa1:CreateShape.ComponentNames>
                                                        <x:String>L1</x:String>
                                                        <x:String>L2</x:String>
                                                        <x:String>L3</x:String>
                                                        <x:String>L4</x:String>
                                                        <x:String>L5</x:String>
                                                        <x:String>L6</x:String>
                                                        <x:String>L10</x:String>
                                                      </asa1:CreateShape.ComponentNames>
                                                      <asa1:CreateShape.ShapeCodes>
                                                        <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                                          <InArgument x:TypeArguments="x:String">BV</InArgument>
                                                        </scg:List>
                                                      </asa1:CreateShape.ShapeCodes>
                                                      <sap:WorkflowViewStateService.ViewState>
                                                        <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                          <x:Boolean x:Key="IsExpanded">True</x:Boolean>
                                                        </scg:Dictionary>
                                                      </sap:WorkflowViewStateService.ViewState>
                                                    </asa1:CreateShape>
                                                    <FlowStep.Next>
                                                      <FlowStep x:Name="__ReferenceID12">
                                                        <sap:WorkflowViewStateService.ViewState>
                                                          <scg:Dictionary x:TypeArguments="x:String, x:Object">
                                                            <av:Point x:Key="ShapeLocation">200,689</av:Point>
                                                            <av:Size x:Key="ShapeSize">200,22</av:Size>
                                                          </scg:Dictionary>
                                                        </sap:WorkflowViewStateService.ViewState>
                                                        <asa1:CreateShape ActivityId="13" DisplayName="S2" Geometry="[Geometry]" sap:VirtualizedContainerService.HintSize="200,22" Links="L5,L7,L9,L8" ShapeNumber="S2" ShowErrors="True" SubassemblyErrorCenter="[SubassemblyErrorCenter]" SubassemblyRunMode="[SubassemblyRunMode]">
                                                          <asa1:CreateShape.ComponentNames>
                                                            <x:String>L5</x:String>
                                                            <x:String>L7</x:String>
                                                            <x:String>L9</x:String>
                                                            <x:String>L8</x:String>
                                                          </asa1:CreateShape.ComponentNames>
                                                          <asa1:CreateShape.ShapeCodes>
                                                            <scg:List x:TypeArguments="InArgument(x:String)" Capacity="4">
                                                              <InArgument x:TypeArguments="x:String">BV.BTL</InArgument>
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
  </Flowchart>
</Activity>'''
    return xaml


def build_pkt(output_pkt: Path):
    src_dir = Path(r'C:\Users\Admin\AppData\Local\Temp\C3DSA\BV_QL13-TRAI.pkt.e57be5ee8b7948f8b23dfcaa0a253b7d')
    guid = 'cb835bfa9ad441a2a43a3792ea44dfa3'

    atc_bytes = (src_dir / f'{guid}.atc').read_bytes()
    cfg_bytes = (src_dir / f'{guid}.cfg').read_bytes()
    pvd_bytes = (src_dir / f'{guid}.pvd').read_bytes()
    emd_bytes = (src_dir / f'{guid}.emd').read_bytes()
    cdmd_bytes = (src_dir / f'{guid}.cdmd').read_bytes()
    png_bytes = (src_dir / 'Untitled.png').read_bytes()

    tpl_png = Path('src/sac_mcp/templates/BV_QL13_TRAI.png')
    tpl_png.write_bytes(png_bytes)

    new_xaml = generate_xaml_bv_trai_goc_p4()
    xaml_bytes = '\ufeff'.encode('utf-8') + new_xaml.encode('utf-8')

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
        zf.writestr('Untitled.png', png_bytes)

    print(f'PKT written to {output_pkt}')


if __name__ == '__main__':
    dest = Path('examples/Sub Assembly/Bo_7_Subassembly_Chuan/12_BV_QL13_TRAI_Goc_P4/BV_QL13-TRAI_Goc_P4.pkt')
    build_pkt(dest)

    desktop_dest = Path(r'C:\Users\Admin\Desktop\BV_QL13-TRAI_Goc_P4.pkt')
    shutil.copy2(dest, desktop_dest)
    print(f'Copied to Desktop: {desktop_dest}')

    rep = PktValidator.validate_pkt(dest, run_native_test=True)
    print('Validation Result:')
    print('  is_valid:', rep.is_valid)
    print('  tier1_opc_ok:', rep.tier1_opc_ok)
    print('  tier2_xaml_ok:', rep.tier2_xaml_ok)
    print('  tier3_native_ok:', rep.tier3_native_ok)
    for issue in rep.issues:
        print(f'  [{issue.severity}] {issue.category}: {issue.message}')
