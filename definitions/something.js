const table_names = ["t11", "t12", "t13"];
table_names.forEach(table_name=>{
    publish(table_name, {
        type: "table",
        description: `${table_name} table is a dynamically generated table`
    })
    .query(ctx=>`SELECT * FROM ${ctx.ref("second_view")}`);
    assert(`assertion1 ${table_name}`).query(ctx=>`SELECT * FROM ${ctx.ref("second_view")} WHERE test>1`);
});
